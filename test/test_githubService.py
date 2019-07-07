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


  def test_getFailsBinary(self):
    url = 'https://github.com/michail-nikolaev/task-force-arma-3-radio/raw/1a4602f3b2861457132a51f27dfa6317a1b8da9b/arma3/@task_force_radio/addons/task_force_radio/anprc152/152.paa'

    result = self.githubService.get(url)

    self.assertIsNone(result)

  def test_getFailsPicture(self):
    url = 'https://github.com/michail-nikolaev/task-force-arma-3-radio/raw/1a4602f3b2861457132a51f27dfa6317a1b8da9b/arma3/@task_force_radio/addons/task_force_radio/anprc152/152.png'

    result = self.githubService.get(url)

    self.assertIsNone(result)

  def test_getFailsWav(self):
    url = 'https://github.com/michail-nikolaev/task-force-arma-3-radio/raw/1a4602f3b2861457132a51f27dfa6317a1b8da9b/ts/radio-sounds/remote_start.wav'

    result = self.githubService.get(url)

    self.assertIsNone(result)

  def test_getFailsRepoBlocked(self):
    url = 'https://api.github.com/repos/mikedm139/UnSupportedAppstore.bundle/issues/20'

    result = self.githubService.get(url)

    self.assertIsNone(result)

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
    
