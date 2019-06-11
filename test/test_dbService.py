import unittest

from psycopg2.extensions import AsIs

from src.error.duplicate import DuplicateError

from src.model.commit import Commit
from src.model.file import File
from src.model.issue import Issue
from src.model.repo import Repo

from src.service.dbService import DbService

from test.testConfigService import TestConfigService

class DbServiceTest(unittest.TestCase):

  @classmethod
  def setUpClass(cls):
    configService = TestConfigService()
    cls.dbService = DbService(configService)

    with open(configService.config['datasource']['test-data']) as testData:
      cls.dbService.cursor.execute(testData.read())
      cls.dbService.connection.commit()

  def test_readRepoId(self):
    repo = Repo(
      url = 'testUrl1', 
      github_id = 1, 
      name = 'testName1')
    expectedId = 1

    resultId = self.dbService.getId(repo)[0]
    
    self.assertEqual(expectedId, resultId)

  def test_addRepoNew(self):
    name = 'test_addRepoNew'
    repo = Repo(
      url = 'test_addRepoNew', 
      github_id = 100, 
      name = name)

    resultId = self.dbService.addRepo(repo)

    self.assertInserted(repo, resultId)

  def test_addRepoExisting(self):
    repo = Repo(
      url = 'testUrl1', 
      github_id = 1, 
      name = 'testUrl1')
    expectedId = 1

    resultId = self.dbService.addRepo(repo)

    self.assertEqual(expectedId, resultId)

  def test_readIssueId(self):
    issue = Issue(
      url = 'testUrl1', 
      github_id = 1, 
      title = 'testTitle1', 
      body = 'testBody1',
      language = 'de',
      repoId = 1)
    expectedId = 1

    resultId = self.dbService.getId(issue)[0]
    
    self.assertEqual(expectedId, resultId)

  def test_addIssueNew(self):
    issue = Issue(
      url = 'test_addIssueNew', 
      github_id = 100, 
      title = 'test_addIssueNew', 
      body = 'test_addIssueNew',
      language = 'de',
      repoId = 1)

    resultId = self.dbService.addIssue(issue)

    self.assertInserted(issue, resultId)

  def test_addIssueExisting(self):
    issue = Issue(
      url = 'testUrl1', 
      github_id = 1, 
      title = 'testTitle1', 
      body = 'testBody1',
      language = 'de',
      repoId = 1)
    expectedId = 1

    resultId = self.dbService.addIssue(issue)

    self.assertEqual(expectedId, resultId)

  def test_readCommitId(self):
    commit = Commit(
      url = 'testUrl1', 
      github_id = 1, 
      message = 'testMessage1',
      language = 'de',
      issueId = 1)
    expectedId = 1

    resultId = self.dbService.getId(commit)[0]
    
    self.assertEqual(expectedId, resultId)

  def test_addCommitNew(self):
    commit = Commit(
      url = 'test_addCommitNew', 
      github_id = 100, 
      message = 'test_addCommitNew', 
      language = 'de',
      issueId = 1)

    resultId = self.dbService.addCommit(commit)

    self.assertInserted(commit, resultId)

  def test_addCommitExisting(self):
    commit = Commit(
      url = 'testUrl1', 
      github_id = 1, 
      message = 'testMessage1',
      language = 'de',
      issueId = 1)
    expectedId = 1

    resultId = self.dbService.addCommit(commit)

    self.assertEqual(expectedId, resultId)

  def test_addFileNew(self):
    file = File(
      sha = 'test_addFileNew',
      url = 'test_addFileNew',
      name = 'test_addFileNew',
      extension = 'ext',
      content = 'test_addFileNew',
      patch = 'test_addFileNew',
      commitId = 1
    )

    resultId = self.dbService.addFile(file)

    self.assertInserted(file, resultId)

  def test_addFileExisting(self):
    file = File(
      sha = 'test_addFileExisting',
      url = 'test_addFileExisting',
      name = 'test_addFileExisting',
      extension = 'ext',
      content = 'test_addFileExisting',
      patch = 'testUrl1',
      commitId = 1
    )
    with self.assertRaises(DuplicateError):
      self.dbService.addFile(file)

  def assertInserted(self, entity, resultId):
    selectQuery = 'select id from %s where id = %s'  

    self.dbService.cursor.execute(selectQuery, (AsIs(entity.table), resultId))
    result = self.dbService.cursor.fetchone()

    self.assertIsNotNone(result)

  @classmethod
  def tearDownClass(cls):
    cls.dbService.connection.close()
    cls.dbService.cursor.close()

if __name__ == '__main__':
    unittest.main()
