import unittest
import requests
import mmh3

from src.service.modelCreationService import ModelCreationService
from src.service.githubService import GithubService

from test.testConfigService import TestConfigService

class ModelCreationServiceTest(unittest.TestCase):

  @classmethod
  def setUpClass(cls):
    configService = TestConfigService()
    with open(configService.config['github']['access-tokens']) as f:
      accessTokens =  f.readlines()

    githubService = GithubService(configService, accessTokens[0])
    cls.modelCreator = ModelCreationService(githubService)

  def test_retrieveRepoFromWithRepository(self):
    event = {
      'repository' : {
        'name' : 'test_retrieveRepoFromWithRepository'
      }
    }

    repo = self.modelCreator.retrieveRepoFrom(event)

    self.assertEqual(event['repository']['name'], repo['name'])

  def test_retrieveRepoFromWithRepo(self):
    event = {
      'repo' : {
        'name' : 'test_retrieveRepoFromWithRepo'
      }
    }

    repo = self.modelCreator.retrieveRepoFrom(event)

    self.assertEqual(event['repo']['name'], repo['name'])

  def test_extractRepoNameAsWhole(self):
    repo = {
        'name' : 'test/test' 
    }

    result = self.modelCreator.extractRepoName(repo)

    self.assertEqual(result, repo['name'])

  def test_extractRepoNameComposed(self):
    repoName = 'owner/name'
    repo = {
        'name' : 'name',
        'owner' : 'owner'
    }

    result = self.modelCreator.extractRepoName(repo)

    self.assertEqual(result, repoName)

  def test_createRepoWithId(self):
      github_id = 1
      name = 'owner/repo'
      url = 'http://localhost'
      event = {
        'repo' : {
          'id' : github_id,
          'name' : name,
          'url' : url
        }
      }

      created = self.modelCreator.createRepo(event)

      self.assertEqual(created.github_id, github_id)
      self.assertEqual(created.name, name)
      self.assertEqual(created.url, url)

  def test_createRepoWithoutId(self):
      name = 'owner/repo'
      url = 'http://localhost'
      event = {
        'repo' : {
          'name' : name,
          'url' : url
        }
      }

      created = self.modelCreator.createRepo(event)

      self.assertIsNone(created.github_id)
      self.assertEqual(created.name, name)
      self.assertEqual(created.url, url)

  def test_createIssue(self):
    github_id = 1
    title = 'Das ist ein Titel'
    body = 'Dieser Text beschreibt etwas'
    url = 'http://localhost'
    issue = {
      'id' : github_id,
      'title' : title,
      'body' : body,
      'labels': [],
      'url' : url
    }
    repoId = 2

    created = self.modelCreator.createIssue(issue, repoId)

    self.assertEqual(created.language, 'de')
    self.assertEqual(created.github_id, github_id)
    self.assertEqual(created.body, body)
    self.assertEqual(created.title, title)
    self.assertEqual(created.labeled, False)
    self.assertEqual(created.url, url)
    self.assertEqual(created.repoId, repoId)

  def test_createCommit(self):
    sha = '1s'
    message = 'Dieser Text beschreibt etwas und hat einen Log: ' \
      'Error: Runtime Exception at line 10'
    url = 'http://localhost'
    commit = {
      'sha' : sha,
      'commit' : {
        'message' : message
      },
      'url' : url
    }
    issueId = 2

    created = self.modelCreator.createCommit(commit, issueId)

    self.assertEqual(created.url, url)
    self.assertEqual(created.github_id, sha)
    self.assertEqual(created.message, message)
    self.assertEqual(created.language, 'de')
    self.assertEqual(created.issueId, issueId)

  def test_createFile(self):
    raw_url = 'https://gist.githubusercontent.com/reuven/5660728/raw/ff8cfe2d80f15b6569c9cf2644163f00105d8612/test-file.txt'
    contents_url = 'http://localhost/contents_url'
    sha = 'sha1'
    patch = 'patch'
    file = {
      'filename' : 'path/to/file.py',
      'raw_url' : raw_url,
      'contents_url' : contents_url,
      'sha' : sha,
      'patch' : patch
    }
    commitId = 2
    content = requests.get(url=raw_url).content.decode('utf-8')
    hash = mmh3.hash128(content, signed = True)
    
    created = self.modelCreator.createFile(file, commitId)

    self.assertEqual(created.url, raw_url)
    self.assertEqual(created.github_id, sha)
    self.assertEqual(created.name, 'path/to/file')
    self.assertEqual(created.extension, '.py')
    self.assertEqual(created.content, content)
    self.assertEqual(created.hash, hash)
