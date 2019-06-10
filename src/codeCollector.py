import json
import os

from src.model.commit import Commit
from src.model.issue import Issue
from src.model.file import File

from src.service.archiveService import ArchiveService
from src.service.dbService import DbService
from src.service.githubService import GithubService
from src.service.issueValidator import IssueValidator
from src.service.configService import ConfigService


class CodeCollector():

  def __init__(self, configService: ConfigService):
    self.archiveService = ArchiveService(configService)
    self.ghService = GithubService(configService)
    self.dbService = DbService(configService)
    self.issueValidator = IssueValidator(configService)

  def collectFor(self, archiveDate):  
    content = self.archiveService.retrieveData(archiveDate)
    for line in content.splitlines(): 
      event = json.loads(line)
      if self.issueValidator.validBugIssue(event):
        self.process(event)

  def process(self, issueEvent):
    issue = issueEvent['payload']['issue']
    repo = issueEvent['repo']
    commits = self.ghService.retrieveCommits(issue, repo)
    if commmits:
      savedRepo = self.dbService.addRepo(repo)
      savedIssue = self.dbService.addIssue(self.createIssue(issue), savedRepo)
      for commit in commits:
        savedCommit = self.dbService.addCommit(self.createCommit(commit, savedIssue))
        for codeFile in commit['files']:
          self.dbService.addFile(self.createFile(codeFile, savedCommit))

  def createIssue(githubIssue, repo):
    lang = langdetect.detect(githubIssue['body']) 
    return Issue(url = githubIssue['url'],
      github_id = githubIssue['id'],
      title = githubIssue['title'],
      body = githubIssue['body'],
      language = lang,
      repo = repo)

  def createCommit(githubCommit, issue):
    lang = langdetect.detect(githubCommit['commit']['message']) 
    return Commit(url = githubCommit['url'],
      github_id = githubCommit['id'],
      messae = githubCommit['commit']['message'],
      language = lang,
      issue = issue)

  def createFile(githubFile, commit):
    filename, fileExtension = os.path.splitext(githubFile['filename'])
    content = self.githubService.get(githubFile['raw_url'])
    return File(url = githubFile['contents_url'],
      sha = githubFile['sha'],
      name = filename,
      extension = fileExtension,
      content = content,
      patch = githubFile['patch'],
      commit = commit)
