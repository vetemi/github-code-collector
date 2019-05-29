import json

from service.archiveService import ArchiveService
from service.dbService import DbService
from service.githubService import GithubService
from service.issueValidator import IssueValidator

from model.issue import Issue

class CodeCollector():

  def __init__(self):
    self.archiveService = ArchiveService()
    self.ghService = GithubService()
    self.dbService = DbService()
    self.issueValidator = IssueValidator()

  def collectFor(self, archiveDate):
    # issue1 = {'title':'errors encountered', 'body':'The function does not work as expected'}
    # issue2 = {'title':'add button', 'body':'It would be cool to have a new button for some function'}
    # issue3 = {'title':'Maybe a bug', 'body':'I am not sure but it seems that I discovered a bug in the processing module. Am I missing something?'}
    # self.issueValidator.validUnlabeldIssue(issue1)
    # self.issueValidator.validUnlabeldIssue(issue2)
    # self.issueValidator.validUnlabeldIssue(issue3)  
    content = self.archiveService.retrieveData(archiveDate)
    for line in content.splitlines(): 
      event = json.loads(line)
      if self.issueValidator.validBugIssue(event):
        self.process(event)

  def process(self, issueEvent):
    commits = self.ghService.retrieveCommits(issueEvent['payload']['issue']['events_url'])
    if commmits:
      repo = self.dbService.addRepo(issueEvent['payload']['repo'])
      issue = self.dbService.addIssue(self.createIssue(issueEvent['payload']['issue']), repo.id)
      for commit in commits:
        savedCommit = self.dbService.addCommit(self.createCommit(commit, issue.id))
        for codeFile in commit['files']:
          self.dbService.addFile(self.createFile(codeFile, savedCommit.id))

  def createIssue(githubIssue, repoId):
    bodyTextOnly = replaceCode(githubIssue['body'])
    ## lang = langdetect.detect(bodyTextOnly) 
    return Issue(githubIssue['url'],
      githubIssue['id'],
      githubIssue['title'],
      githubIssue['body'],
      bodyTextOnly,
      lang,
      repoId)

  def createCommit(githubIssue, issueId):
    bodyTextOnly = replaceCode(githubIssue['body'])
    ## lang = langdetect.detect(bodyTextOnly) 
    return Issue(githubIssue['url'],
      githubIssue['id'],
      githubIssue['title'],
      githubIssue['body'],
      bodyTextOnly,
      lang,
      repoId)

def createFile(githubIssue, issueId):
    bodyTextOnly = replaceCode(githubIssue['body'])
    ## lang = langdetect.detect(bodyTextOnly) 
    return Issue(githubIssue['url'],
      githubIssue['id'],
      githubIssue['title'],
      githubIssue['body'],
      bodyTextOnly,
      lang,
      repoId)
