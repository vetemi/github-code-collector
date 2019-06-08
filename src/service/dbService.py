import psycopg2

from service.configService import ConfigService

from model.repo import Repo

class DbService:

  def __init__(self, configService):
    self.connection = psycopg2.connect(
      user = configService.config['datasource']['user'],
      password = configService.config['datasource']['password'],
      host = configService.config['datasource']['host'],
      port = configService.config['datasource']['port'],
      database = configService.config['datasource']['database'])
    self.cursor = self.connection.cursor()

    if configService.config.getboolean('Datasource', 'drop-first'):
      with open(configService.config['datasource']['drop-script']) as dropScript:
        self.cursor.execute(dropScript.read())
        self.connection.commit()

    with open(configService.config['datasource']['schema']) as schema:
      self.cursor.execute(schema.read())
      self.connection.commit()

  def addRepo(self, repo):
    repoId = self.getRepoId(repo)
    if repoId:
      return repoId
    else:
      return self.insertRepo(repo)
  
  def getRepoId(repo: Repo):
    selectQuery = 'select id from repositories where github_id = %s and url = %s'  
    
    self.cursor.execute(selectQuery, (repo.github_id, repo.url))
    return self.cursor.fetchone()
 
  def insertRepo(repo: Repo):
    insertQuery = 'insert into repositories(github_id, url, name) values (%s,%s,%s) returning id'

    self.cursor.execute(insertQuery, (repo.github_id, repo.url, repo.name))
    self.cursor.commit()
    return self.cursor.fetchone()[0]

  def addIssue(self, repo):
    return None

  def addCommit(self, repo):
    return None

  def addFile(self, repo):
    return None
