from src.service.configService import ConfigService
from src.service.bugDetector import BugDetector

class IssueValidator:

  def __init__(self, configService: ConfigService):
    self.bugDetector = BugDetector(configService)
    self.initBugLabels()

  def validBugIssue(self, event):
    if (event['type'] == 'IssuesEvent' 
      and event['payload']['action'] == 'closed' 
      and not isinstance(event['payload']['issue'], int)):

      if event['payload']['issue']['labels']:
        return self.validLabeledIssue(event['payload']['issue']['labels'])
      else:
        return self.validUnlabeledIssue(event['payload']['issue'])

    return False

  def validLabeledIssue(self, labels):
    for label in labels:
      if label['name'].lower() in self.validBugLabels:
        return True
    return False

  def validUnlabeledIssue(self, issue):
    return self.bugDetector.isBug(issue)

  def initBugLabels(self):
    self.validBugLabels = []
    self.validBugLabels.append('bug')
    self.validBugLabels.append('type: bug')
    self.validBugLabels.append('type-defect')
    self.validBugLabels.append('security vulnerability')
    self.validBugLabels.append('vulnerability')
    self.validBugLabels.append('regression')
    self.validBugLabels.append('type:bug')
    self.validBugLabels.append('crash')
    self.validBugLabels.append('defect')
    self.validBugLabels.append('kind/bug')
    self.validBugLabels.append('type/bug')
    self.validBugLabels.append('error')
    self.validBugLabels.append('type.bug')
    self.validBugLabels.append('confirmed bug')
    self.validBugLabels.append('type-bug')
    self.validBugLabels.append('type_bug')
    self.validBugLabels.append('bugs')
    self.validBugLabels.append('critical bug')
    self.validBugLabels.append('major bug')
    self.validBugLabels.append('[type] bug')
    self.validBugLabels.append('bug :bug:')
    self.validBugLabels.append('kind:bug')
    self.validBugLabels.append('t:bug')
    self.validBugLabels.append('t-bug')
    self.validBugLabels.append('type: bug')
    self.validBugLabels.append('t: bug')
