import unittest

from src.codeCollector import CodeCollector

from test.testConfigService import TestConfigService

class CodeCollectorTest(unittest.TestCase):

  @classmethod
  def setUpClass(cls):
    configService = TestConfigService()
    cls.codeCollector = CodeCollector(configService)

  def test_createIssue(self):
    issue = {
      'id' : 1,
      'title' : 'Das ist ein Titel',
      'body' : 'Dieser Text beschreibt etwas',
      'url' : 'http://localhost'
    }
    repoId = 1

    created = self.codeCollector.createIssue(issue, repoId)

    self.assertEqual(created.language, 'de')
