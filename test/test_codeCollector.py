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


  def test_processEvent(self):
    event = {'created_at': '2013-07-27T06:44:11-07:00', 'payload': {'action': 'closed', 'issue': 17242353, 'number': 10}, 'public': True, 'type': 'IssuesEvent', 'url': 'https://github.com/sillyotter/Theodorus2/issues/10', 'actor': 'sillyotter', 'actor_attributes': {'login': 'sillyotter', 'type': 'User', 'gravatar_id': '47d047d4667501ab21dac35ca8913992', 'name': '', 'blog': 'http://sillyotter.github.io/', 'email': 'da39a3ee5e6b4b0d3255bfef95601890afd80709'}, 'repository': {'id': 11594263, 'name': 'Theodorus2', 'url': 'https://github.com/sillyotter/Theodorus2', 'description': 'A new and improved SQLite query tool', 'watchers': 1, 'stargazers': 1, 'forks': 0, 'fork': False, 'size': 1320, 'owner': 'sillyotter', 'private': False, 'open_issues': 8, 'has_issues': True, 'has_downloads': True, 'has_wiki': True, 'language': 'C#', 'created_at': '2013-07-22T15:44:57-07:00', 'pushed_at': '2013-07-27T06:43:11-07:00', 'master_branch': 'master'}}

    self.codeCollector.processEvent(event)
