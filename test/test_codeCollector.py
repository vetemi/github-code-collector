import unittest

from src.codeCollector import CodeCollector

from test.testConfigService import TestConfigService

class CodeCollectorTest(unittest.TestCase):

  @classmethod
  def setUpClass(cls):
    configService = TestConfigService()
    with open(configService.config['github']['access-tokens']) as f:
      accessTokens =  f.readlines()

    cls.codeCollecotr = CodeCollector(configService, accessTokens[0])

  def test_retrieveRepoFromWithRepo(self):
    event = {
      'repo' : {
        'name' : 'test_retrieveRepoFromWithRepo'
      }
    }

    repo = self.codeCollecotr.retrieveRepoFrom(event)

    self.assertEqual(event['repo']['name'], repo['name'])

  def test_retrieveRepoFromWithRepository(self):
    event = {
      'repository' : {
        'name' : 'test_retrieveRepoFromWithRepository'
      }
    }

    repo = self.codeCollecotr.retrieveRepoFrom(event)

    self.assertEqual(event['repository']['name'], repo['name'])

  def test_retrieveValidIssueFromPayload(self):
    repo = { 'name' : 'test/retrieveValidIssueFromSuccess' }
    event = {
      'type' : 'IssuesEvent',
      'payload': {
        'issue': {
          'body' : 'test_retrieveValidIssueFromSuccess',
          'title' : 'test_retrieveValidIssueFromSuccess',
          'labels' : [
            { 'name' :  'bug' }
          ]
        },
        'action': 'closed'
      }
    }

    issue = self.codeCollecotr.retrieveValidIssueFrom(event, repo)
    print(issue)

    self.assertEqual(event['payload']['issue']['title'], issue['title'])

  def test_retrieveValidIssueFromRequest(self):
    title = 'Duplicates when sorting'
    repo = { 'name' : 'codeschluss/wupportal' }
    event = {
      'type' : 'IssuesEvent',
      'payload': {
        'issue': 98,
        'action': 'closed'
      }
    }

    issue = self.codeCollecotr.retrieveValidIssueFrom(event, repo)

    self.assertEqual(title, issue['title'])

