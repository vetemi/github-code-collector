import json
import gzip

from src.model.patch import Patch

from src.service.archiveService import ArchiveService
from src.service.configService import ConfigService
from src.service.dbService import DbService
from src.service.githubService import GithubService
from src.service.issueValidator import IssueValidator
from src.service.modelCreationService import ModelCreationService

class CodeCollector():

  def __init__(self, configService: ConfigService, accessToken):
    self.archiveService = ArchiveService(configService)
    self.ghService = GithubService(configService, accessToken)
    self.dbService = DbService(configService)
    self.issueValidator = IssueValidator(configService)
    self.modelCreator = ModelCreationService(self.ghService)
    self.failedEvent = None

  def processFor(self, archiveDate):
    event = None
    try:
      if not self.dbService.archiveDateExists(archiveDate):
        content = self.archiveService.retrieveData(archiveDate)
        for line in content:
          event = json.loads(line.decode())
          if self.isValid(event):
            self.processEvent(event)
        self.dbService.addArchiveDate(archiveDate, True)
    except Exception as error:
      self.failedEvent = event
      self.dbService.addArchiveDate(archiveDate, False)
      raise error
  
  def isValid(self, event):
    return event['type'] == 'IssuesEvent' and event['payload']['action'] == 'closed'

  def processEvent(self, event):
    repo = self.modelCreator.createRepo(event)
    githubIssue = self.retrieveIssueFrom(event, repo)
    if githubIssue:
      self.collectData(githubIssue, repo)

  def retrieveIssueFrom(self, event, repo):
    issue = event['payload']['issue']
    if isinstance(issue, int):
      issue = self.ghService.retrieveIssue(repo, event['payload']['number'])
    if issue and self.issueValidator.validBugIssue(issue):
      return issue

  def collectData(self, issue, repo):
    commits = self.ghService.retrieveCommits(issue, repo)
    if commits:
      repoId = self.dbService.addRepo(repo)
      issueId = self.dbService.addIssue(self.modelCreator.createIssue(issue, repoId))
      for commit in commits:
        commitId = self.dbService.addCommit(self.modelCreator.createCommit(commit, issueId))
        if commitId and 'files' in commit:
          self.collectFilepatches(commit['files'], commitId)

  def collectFilepatches(self, files, commitId):
    for codeFile in files:
      if (codeFile['raw_url'] and 'patch' in codeFile):
        file = self.modelCreator.createFile(codeFile, commitId)
        if file:
          fileId = self.dbService.addFile(file)
          self.dbService.addPatch(self.modelCreator.createPatch(codeFile['patch'], fileId))   
