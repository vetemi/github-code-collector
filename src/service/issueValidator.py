from service.configService import ConfigService

from tensorflow.keras.models import load_model
import dill

class IssueValidator:

  def __init__(self):
    self.configService = ConfigService()

    self.initIssueDetector()
    self.initBugLabels()

  def validBugIssue(self, event):
    if (event['type'] == 'IssuesEvent' 
      and event['payload']['action'] == 'closed' 
      and not isinstance(event['payload']['issue'], int)):

      if event['payload']['issue']['labels']:
        # return validLabeledIssue(event['payload']['issue']['labels'])
        return False
      else:
        return self.validUnlabeldIssue(event['payload']['issue'])

    return False

  def validLabeledIssue(self, labels):
    for label in event['payload']['issue']['labels']:
      if label['name'].lower() in self.validBugLabels:
        return True
    return False

  def validUnlabeldIssue(self, issue):
    if not issue['body'] or not issue['body']:
      return False   

    vecTitle = self.titlePreproc.transform([issue['title']])
    vecBody = self.bodyPreproc.transform([issue['body']])
    probs = self.issueDetector.predict(x=[vecBody, vecTitle]).tolist()[0]
    if probs[0] >= 0.5 and probs[0] <= 0.7:
      print(f'probs: {probs[0]} for issue: ' + issue['url'])
      return True

  def initIssueDetector(self):
    self.issueDetector = load_model(self.configService.config['issuedetection']['model'])
    self.threshold = float(self.configService.config['issuedetection']['threshold'])

    with open(self.configService.config['issuedetection']['title-preprocessor'], 'rb') as f:
      self.titlePreproc = dill.load(f)

    with open(self.configService.config['issuedetection']['body-preprocessor'], 'rb') as f:
      self.bodyPreproc = dill.load(f)

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
