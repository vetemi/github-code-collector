from service.configService import ConfigService

import psycopg2

class DbService:


  def __init__(self):
    configService = ConfigService()
    self.connection = psycopg2.connect(
      user = configService.config['datasource']['user'],
      password = configService.config['datasource']['password'],
      host = configService.config['datasource']['host'],
      port = configService.config['datasource']['port'],
      database = configService.config['datasource']['database'])
    self.dbCursor = self.connection.cursor()

    with open(configService.config['datasource']['schema']) as schema:
      self.dbCursor.execute(schema.read())
      self.connection.commit()

  def addRepo(self, repo):
    if self.repoExists(repo):
      return self.getRepo(repo)
    else:
      return self.insertRepo(repo)
  
  def repoExists(repo):
    return None

  def insertRepo(repo):
    return None

  def addIssue(self, repo):
    return None

  def addCommit(self, repo):
    return None

  def addFile(self, repo):
    return None
