import unittest

from src.service.issueValidator import IssueValidator

from test.testConfigService import TestConfigService

class IssueValidatorTest(unittest.TestCase):

  @classmethod
  def setUpClass(cls):
    configService = TestConfigService()
    cls.issueValidator = IssueValidator(configService)

  def test_validLabeledIssue(self):
    validBugLabels = []
    validBugLabels.append({'name':'bug'})
    
    result = self.issueValidator.validLabeledIssue(validBugLabels)

    self.assertTrue(result)

  def test_invalidLabeledIssue(self):
    validBugLabels = []
    validBugLabels.append({'name':'not a bug'})
    
    result = self.issueValidator.validLabeledIssue(validBugLabels)

    self.assertFalse(result)

  def test_validUnLabeledIssue(self):
    issue = {
      'title':'Error occured',
      'body':'I discovered a bug, please fix it'
    }
    
    result = self.issueValidator.validUnlabeledIssue(issue)

    self.assertTrue(result)

  def test_invalidLabeledIssue(self):
    issue = {
      'title':'New function required',
      'body':'I would be nice to have a new function'
    }

    result = self.issueValidator.validUnlabeledIssue(issue)

    self.assertFalse(result)


  def test_validBugIssue(self):
    event = {
      'type' : 'IssuesEvent',
      'payload' : {
        'action' : 'closed',
        'issue': {
          'labels': [
            { 'name' : 'bug'}
          ] 
        }
      }
    }

    result = self.issueValidator.validBugIssue(event)

    self.assertTrue(result)

  def test_invalidBugIssue(self):
    event = {
      'type' : 'IssuesEvent',
      'payload' : {
        'action' : 'closed',
        'issue': 1
      }
    }

    result = self.issueValidator.validBugIssue(event)

    self.assertFalse(result)
