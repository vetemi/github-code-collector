import unittest
from datetime import datetime

from psycopg2.extensions import AsIs

from src.model.commit import Commit
from src.model.file import File
from src.model.issue import Issue
from src.model.patch import Patch
from src.model.repo import Repo

from src.service.dbService import DbService
from src.codeCollector import CodeCollector

from test.testConfigService import TestConfigService

class DbServiceTest(unittest.TestCase):

  @classmethod
  def setUpClass(cls):
    cls.configService = TestConfigService()
    cls.dbService = DbService(cls.configService)
    DbService.initDb(cls.configService, cls.dbService.cursor, cls.dbService.connection)

    with open(cls.configService.config['datasource']['test-data']) as testData:
      cls.dbService.cursor.execute(testData.read())
      cls.dbService.connection.commit()

  def test_readRepoId(self):
    repo = Repo(
      url = 'testUrl1', 
      github_id = 1, 
      name = 'testName1')
    expectedId = 1

    resultId = self.dbService.getById(repo)[0]
    
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
      language = None,
      repoId = 1)
    expectedId = 1

    resultId = self.dbService.getByIdAndUrl(issue)[0]
    
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
      github_id = 'testSha1', 
      message = 'testMessage1',
      language = 'de',
      issueId = 1)
    expectedId = 1

    resultId = self.dbService.getById(commit)[0]
    
    self.assertEqual(expectedId, resultId)

  def test_addCommitNew(self):
    commit = Commit(
      url = 'test_addCommitNew', 
      github_id = 'test_addCommitNew', 
      message = 'test_addCommitNew', 
      language = 'de',
      issueId = 1)

    resultId = self.dbService.addCommit(commit)

    self.assertInserted(commit, resultId)

  def test_addCommitExisting(self):
    commit = Commit(
      url = 'testUrl1', 
      github_id = 'testSha1', 
      message = 'testMessage1',
      language = 'de',
      issueId = 1)

    resultId = self.dbService.addCommit(commit)

    self.assertIsNone(resultId)

  def test_addFileNew(self):
    file = File(
      github_id = 'test_addFileNew',
      url = 'test_addFileNew',
      name = 'test_addFileNew',
      extension = 'testExt',
      content = 'test_addFileNew',
      hash = 100,
      commitId = 1
    )

    resultId = self.dbService.addFile(file)

    self.assertInserted(file, resultId)

  def test_addFile(self):
    file = File(
      github_id = 'test_addFile',
      url = 'test_addFile',
      name = 'test_addFile',
      extension = 'testExt1',
      content = 'testContent1',
      hash = 1,
      commitId = 1
    )
    expectedId = 1

    resultId = self.dbService.addFile(file)

    self.assertEqual(resultId, expectedId)

  def test_addPatchNew(self):
    patch = Patch(
      content = 'test_addPatchNew',
      fileId = 1
    )

    resultId = self.dbService.addPatch(patch)

    self.assertInserted(patch, resultId)

  def assertInserted(self, entity, resultId):
    selectQuery = 'select id from %s where id = %s'  

    self.dbService.cursor.execute(selectQuery, (AsIs(entity.table), resultId))
    result = self.dbService.cursor.fetchone()

    self.assertIsNotNone(result)

  def test_addArchiveNew(self):
    archiveDate = datetime(2099, 2, 12, 0)
    succeeded = True

    self.dbService.addArchiveDate(archiveDate, succeeded)
  
    string = archiveDate.strftime(self.configService.config ['date']['format'])
    self.dbService.cursor.execute(
      f"select id from archive_dates where date = '{string}'"
    )

    self.assertIsNotNone(self.dbService.cursor.fetchone())

  def test_archiveDateExists(self):
    archiveDate = datetime(2019, 6, 22, 0)

    result = self.dbService.archiveDateExists(archiveDate)

    self.assertIsNotNone(result)

  def test_archiveDateNotExists(self):
    archiveDate = datetime(2000, 6, 22, 0)

    result = self.dbService.archiveDateExists(archiveDate)

    self.assertIsNone(result)

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
