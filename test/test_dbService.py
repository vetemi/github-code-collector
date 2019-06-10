import unittest

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
    repo = Repo(url='testUrl1', github_id=1, name='testName1')
    expectedId = 1

    resultId = self.dbService.getRepoId(repo)[0]
    
    self.assertEqual(expectedId, resultId)

  def test_addRepoIdNew(self):
    repo = Repo(url='test_addRepoIdNew', github_id=100, name='test_addRepoIdNew')
    expectedId = 2

    resultId = self.dbService.addRepo(repo)

    self.assertEqual(expectedId, resultId)

  def test_addRepoIdExisting(self):
    repo = Repo(url='testUrl1', github_id=1, name='testUrl1')
    expectedId = 1

    resultId = self.dbService.addRepo(repo)

    self.assertEqual(expectedId, resultId)

  @classmethod
  def tearDownClass(cls):
    cls.dbService.connection.close()
    cls.dbService.cursor.close()

if __name__ == '__main__':
    unittest.main()
