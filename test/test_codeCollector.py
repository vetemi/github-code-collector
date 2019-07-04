import unittest

from src.model.repo import Repo

from src.codeCollector import CodeCollector

from test.testConfigService import TestConfigService

class CodeCollectorTest(unittest.TestCase):

  @classmethod
  def setUpClass(cls):
    configService = TestConfigService()
    with open(configService.config['github']['access-tokens']) as f:
      accessTokens =  f.readlines()

    cls.codeCollector = CodeCollector(configService, accessTokens[0])

  def test_isValidTrue(self):
    event = {
      'type' : 'IssuesEvent',
      'payload': {
        'issue': {
          'body' : 'test_retrieveIssueFromPayload',
          'title' : 'test_retrieveIssueFromPayload',
          'labels' : [
            { 'name' :  'bug' }
          ]
        },
        'action': 'closed'
      }
    }

    result = self.codeCollector.isValid(event)

    self.assertTrue(result)

  def test_isValidFalse(self):
    event = {
      'type' : 'IssuesEvent',
      'payload': {
        'issue': {
          'body' : 'test_retrieveIssueFromPayload',
          'title' : 'test_retrieveIssueFromPayload',
          'labels' : [
            { 'name' :  'bug' }
          ]
        },
        'action': 'reopened'
      }
    }

    result = self.codeCollector.isValid(event)

    self.assertFalse(result)

  def test_retrieveIssueFromPayload(self):
    repo = Repo(
      github_id = 1000,
      url = 'someurl',
      name = 'codeschluss/wupportal'
    )
    event = {
      'type' : 'IssuesEvent',
      'payload': {
        'issue': {
          'body' : 'test_retrieveIssueFromPayload',
          'title' : 'test_retrieveIssueFromPayload',
          'labels' : [
            { 'name' :  'bug' }
          ]
        },
        'action': 'closed'
      }
    }

    issue = self.codeCollector.retrieveIssueFrom(event, repo)

    self.assertEqual(event['payload']['issue']['title'], issue['title'])

  def test_retrieveIssueFromRequest(self):
    title = 'Duplicates when sorting'
    repo = Repo(
      github_id = 1000,
      url = 'someurl',
      name = 'codeschluss/wupportal'
    )
    event = {
      'type' : 'IssuesEvent',
      'payload': {
        'issue': 46897,
        'action': 'closed',
        'number': 98
      }
    }

    issue = self.codeCollector.retrieveIssueFrom(event, repo)

    self.assertEqual(title, issue['title'])
