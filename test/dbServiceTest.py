import unittest
import src
import src.service

from src.service.dbService import DbService

from src.model.repo import Repo

from testConfigService import TestConfigService

class DbServiceTest(unittest.TestCase):

  @classmethod
  def setUpClass(cls):
    configService = TestConfigService()
    cls.dbService = DbService(configService)

    with open(configService.config['datasource']['test-data']) as testData:
      self.dbCursor.execute(testData.read())
      self.connection.commit()


  def test_readRepoId(self):
    repo = Repo(url='testUrl1', github_id=1, name='testName1')
    expectedId = 1

    resultId = self.dbService.getRepoId(repo)
    
    self.assertEqual(expectedId, resultId)

  @classmethod
  def tearDownClass(cls):
    cls.dbService.connection.close()
    cls.dbService.cursor.close()

if __name__ == '__main__':
    unittest.main()
