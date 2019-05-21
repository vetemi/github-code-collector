from service.configService import ConfigService

import mysql.connector

class DbService:

  def __init__(self):
    configService = ConfigService()
    self.codeDb = mysql.connector.connect(
      host=configService.config['Datasource']['url'],
      user=configService.config['Datasource']['user'],
      passwd=configService.config['Datasource']['password']
    )
    self.dbCursor = self.codeDb.cursor()

    if configService.config.getboolean('Datasource', 'drop-first'):
      self.dbCursor.execute("DROP DATABASE codeDB")
      self.codeDb.commit()
      self.dbCursor.execute("CREATE DATABASE codeDB")
      self.codeDb.commit()

      with open(configService.config['Datasource']['schema']) as schema:
        self.dbCursor.execute(schema.read(), multi=True)
        self.codeDb.commit()

  def addRepo(self, repo):
    return None



