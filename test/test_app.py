import unittest
from datetime import datetime

import src.app as App
from src.service.dbService import DbService
from test.testConfigService import TestConfigService

class AppTest(unittest.TestCase):

  def test_getStartDateDefault(self):
    configService = TestConfigService()
    dbService = DbService(configService)
    DbService.initDb(configService, dbService.cursor, dbService.connection)
    
    expectedDate = App.defaultStartDate
    
    startDate = App.getStartDate(dbService.cursor)

    self.assertEqual(expectedDate, startDate)

  def test_getStartDateDefault(self):
    configService = TestConfigService()
    dbService = DbService(configService)
    DbService.initDb(configService, dbService.cursor, dbService.connection)
    with open(configService.config['datasource']['test-data']) as testData:
      dbService.cursor.execute(testData.read())
      dbService.connection.commit()

    expectedDate = datetime(2100, 6, 22, 1)
    
    startDate = App.getStartDate(dbService.cursor)

    self.assertEqual(expectedDate, startDate)
