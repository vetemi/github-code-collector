import concurrent.futures
import json
import os
import requests

import mmh3
import langdetect

from src.error.InvalidTokenError import InvalidTokenError

from src.model.commit import Commit
from src.model.file import File
from src.model.issue import Issue
from src.model.patch import Patch
from src.model.repo import Repo

from src.service.archiveService import ArchiveService
from src.service.dbService import DbService
from src.service.githubService import GithubService
from src.service.issueValidator import IssueValidator
from src.service.configService import ConfigService

class CodeCollector():

  def __init__(self, configService: ConfigService, accessToken):
    self.archiveService = ArchiveService(configService)
    self.ghService = GithubService(configService, accessToken)
    self.dbService = DbService(configService)
    self.issueValidator = IssueValidator(configService)

  def collectFor(self, archiveDate):
    event = None
    try:
      if self.dbService.archiveDateExists(archiveDate):
        return None
      content = self.archiveService.retrieveData(archiveDate)
      lines = content.splitlines()
      for line in lines:
        event = json.loads(line)
        if self.issueValidator.validBugIssue(event):
          self.process(event)
    except InvalidTokenError as error:
      self.dbService.addArchiveDate(archiveDate, False)
      raise error
    except Exception as error:
      self.failedEvent = event
      self.dbService.addArchiveDate(archiveDate, False)
      raise error
    self.dbService.addArchiveDate(archiveDate, True)

  def process(self, issueEvent):
    issue = issueEvent['payload']['issue']
    repo = issueEvent['repo']
    commits = self.ghService.retrieveCommits(issue, repo)
    if commits:
      repoId = self.dbService.addRepo(self.createRepo(repo))
      issueId = self.dbService.addIssue(self.createIssue(issue, repoId))
      for commit in commits:
        commitId = self.dbService.addCommit(self.createCommit(commit, issueId))
        if commitId:
          self.processFilepatches(commit, commitId)

  def processFilepatches(self, commit, commitId):
    for codeFile in commit['files']:
      if (codeFile['raw_url'] and 'patch' in codeFile):
        fileId = self.dbService.addFile(self.createFile(codeFile, commitId))
        self.dbService.addPatch(Patch(codeFile['patch'], fileId))   
                
  def createRepo(self, githubRepo):
    return Repo(
      url = githubRepo['url'],
      github_id = githubRepo['id'],
      name = githubRepo['name']) 

  def createIssue(self, githubIssue, repoId):
    lang = self.detectLang(githubIssue['body'])
    return Issue(url = githubIssue['url'],
      github_id = githubIssue['id'],
      title = githubIssue['title'],
      body = githubIssue['body'],
      language = lang,
      repoId = repoId)

  def createCommit(self, githubCommit, issueId):
    lang = self.detectLang(githubCommit['commit']['message'])
    return Commit(url = githubCommit['url'],
      github_id = githubCommit['sha'],
      message = githubCommit['commit']['message'],
      language = lang,
      issueId = issueId)

  def detectLang(self, text):
    if text:
      try:
        return langdetect.detect(text) 
      except:
        pass

  def createFile(self, githubFile, commitId):
    filename, fileExtension = os.path.splitext(githubFile['filename'])
    content = self.retrieveFile(githubFile['raw_url'])
    hash = mmh3.hash128(content, signed = True)
    return File(url = githubFile['raw_url'],
      github_id = githubFile['sha'],
      name = filename,
      extension = fileExtension,
      content = content,
      hash = hash,
      commitId = commitId)

  def retrieveFile(self, url):
    try:
      return self.retrieveFile(url)
    except requests.exceptions.ConnectionError:
      return self.retrieveFile(url)
