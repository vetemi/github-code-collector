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
        return validLabeledIssue(event['payload']['issue']['labels'])
      else:
        return validUnlabeldIssue(event['payload']['issue'])

    return False

  def validLabeledIssue(self, labels):
    for label in event['payload']['issue']['labels']:
      if label['name'].lower() in self.validBugLabels:
        return True
    return False

  def validUnlabeldIssue(self, issue):
    vecTitle = self.titlePreproc.transform([issue['title']])
    vecBody = self.bodyPreproc.transform([issue['body']])
    class_names=['bug', 'feature_request/question']
    probs = self.issueDetector.predict(x=[vecBody, vecTitle]).tolist()[0]
    print({k:v for k,v in zip(class_names, probs)})

  def initIssueDetector(self):
    self.issueDetector = load_model(self.configService.config['issuedetection']['model'])

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
