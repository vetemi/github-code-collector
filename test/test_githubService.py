import unittest

from src.model.repo import Repo

from src.service.githubService import GithubService

from test.testConfigService import TestConfigService

class GithubServiceTest(unittest.TestCase):

  @classmethod
  def setUpClass(cls):
    configService = TestConfigService()
    with open(configService.config['github']['access-tokens']) as f:
      accessTokens =  f.readlines()

    cls.githubService = GithubService(configService, accessTokens[0])

  def test_retrieveCommitsFromEventsContaining(self):
    issue = {
      'events_url' : 'https://api.github.com/repos/websocket-client/websocket-client/issues/141/events'
    }

    commits = self.githubService.retrieveCommitsFromEvents(issue)

    self.assertEqual(len(commits), 2)

  def test_retrieveCommitsFromEventsNotContaining(self):
    issue = {
      'events_url' : 'https://api.github.com/repos/poole/lanyon/issues/81/events'
    }

    commits = self.githubService.retrieveCommitsFromEvents(issue)

    self.assertEqual(len(commits), 0)

  def test_retrieveCommitsFromPullRequest(self):
    repo = Repo(
      github_id = 1000,
      url = 'someurl',
      name = 'codeschluss/wupportal'
    )

    issue = {
      'number' : 91
    }

    commits = self.githubService.retrieveCommitsFromPullRequest(issue, repo)
    
    self.assertEqual(len(commits), 9)

  def test_retrieveIssue(self):
    title = 'Duplicates when sorting'
    repo = Repo(
      github_id = 1000,
      url = 'someurl',
      name = 'codeschluss/wupportal'
    )
    issueNumber = 98

    issue = self.githubService.retrieveIssue(repo, issueNumber)

    self.assertEqual(title, issue['title'])
    
