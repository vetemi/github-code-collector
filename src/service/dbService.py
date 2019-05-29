from service.configService import ConfigService

import mysql.connector

class DbService:

  def __init__(self):
    configService = ConfigService()
    self.codeDb = mysql.connector.connect(
      host=configService.config['datasource']['url'],
      user=configService.config['datasource']['user'],
      passwd=configService.config['datasource']['password']
    )
    self.dbCursor = self.codeDb.cursor()

    if configService.config.getboolean('datasource', 'drop-first'):
      self.dbCursor.execute('DROP DATABASE ' 
        + configService.config['datasource']['database'])
      self.codeDb.commit()

      self.dbCursor.execute('CREATE DATABASE '
        + configService.config['datasource']['database'])
      self.codeDb.commit()

      with open(configService.config['datasource']['schema']) as schema:
        self.dbCursor.execute(schema.read(), multi=True)
        self.codeDb.commit()

  def addRepo(self, repo):
    return None



