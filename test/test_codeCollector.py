import unittest
import requests
import mmh3

from src.codeCollector import CodeCollector

from test.testConfigService import TestConfigService

class CodeCollectorTest(unittest.TestCase):

  @classmethod
  def setUpClass(cls):
    configService = TestConfigService()
    cls.codeCollector = CodeCollector(configService)

  def test_createRepo(self):
      github_id = 1
      name = 'owner/repo'
      url = 'http://localhost'
      repo = {
        'id' : github_id,
        'name' : name,
        'url' : url
      }

      created = self.codeCollector.createRepo(repo)

      self.assertEqual(created.github_id, github_id)
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
      'url' : url
    }
    repoId = 2

    created = self.codeCollector.createIssue(issue, repoId)

    self.assertEqual(created.language, 'de')
    self.assertEqual(created.github_id, github_id)
    self.assertEqual(created.body, body)
    self.assertEqual(created.title, title)
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

    created = self.codeCollector.createCommit(commit, issueId)

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
    content = requests.get(url=raw_url).content
    hash = mmh3.hash128(content, signed = True)
    
    created = self.codeCollector.createFile(file, commitId)

    self.assertEqual(created.url, raw_url)
    self.assertEqual(created.github_id, sha)
    self.assertEqual(created.name, 'path/to/file')
    self.assertEqual(created.extension, '.py')
    self.assertEqual(created.content, content)
    self.assertEqual(created.hash, hash)
