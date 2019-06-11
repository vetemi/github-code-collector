import psycopg2
from psycopg2.extensions import AsIs
from psycopg2.errors import UniqueViolation

from src.error.duplicate import DuplicateError

from src.model.commit import Commit
from src.model.file import File
from src.model.issue import Issue
from src.model.repo import Repo

from src.service.configService import ConfigService

class DbService:

  def __init__(self, configService):
    self.connection = psycopg2.connect(
      user = configService.config['datasource']['user'],
      password = configService.config['datasource']['password'],
      host = configService.config['datasource']['host'],
      port = configService.config['datasource']['port'],
      database = configService.config['datasource']['database'])
    self.cursor = self.connection.cursor()

    if configService.config.getboolean('datasource', 'drop-first'):
      with open(configService.config['datasource']['drop-script']) as dropScript:
        self.cursor.execute(dropScript.read())
        self.connection.commit()

    with open(configService.config['datasource']['schema']) as schema:
      self.cursor.execute(schema.read())
      self.connection.commit()

  def addRepo(self, repo: Repo):
    insertQuery = 'insert into repositories(github_id, url, name) ' \
      'values (%s,%s,%s) returning id'
    params = (repo.github_id, repo.url, repo.name)
    return self.insert(insertQuery, params, repo)

  def addIssue(self, issue: Issue):
    insertQuery = 'insert into issues(github_id, url, title, body, language, repository_id)' \
      'values (%s,%s,%s,%s,%s,%s) returning id'
    params = (issue.github_id, issue.url, issue.title, issue.body, issue.language, issue.repoId)
    return self.insert(insertQuery, params, issue)

  def addCommit(self, commit: Commit):
    insertQuery = 'insert into commits(github_id, url, message, language, issue_id)' \
      'values (%s,%s,%s,%s,%s) returning id'
    params = (commit.github_id, commit.url, commit.message, commit.language, commit.issueId)
    return self.insert(insertQuery, params, commit)
 
  def insert(self, insertQuery, params, entity):
    try:
      self.cursor.execute(insertQuery, params)
      self.connection.commit()
      return self.cursor.fetchone()[0]
    except UniqueViolation as ex:
      self.connection.rollback()
      return self.getId(entity)[0]

  def getId(self, entity):
    selectQuery = 'select id from %s where github_id = %s and url = %s'  

    self.cursor.execute(selectQuery, (AsIs(entity.table), entity.github_id, entity.url))
    return self.cursor.fetchone()

  def addFile(self, file: File):
    try:
      insertQuery = 'insert into files(sha, url, name, extension, content, patch, commit_id)' \
        'values (%s, %s, %s, %s, %s, %s, %s) returning id'

      self.cursor.execute(insertQuery, 
        (file.sha, file.url, file.name, file.extension, file.content, file.patch, file.commitId))
      
      self.connection.commit()
      return self.cursor.fetchone()[0]
    except UniqueViolation as ex:
      self.connection.rollback()
      raise DuplicateError('Patch already exists')
