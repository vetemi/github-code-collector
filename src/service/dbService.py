import psycopg2
from psycopg2.extensions import AsIs, quote_ident
from psycopg2.errors import UniqueViolation

from src.model.commit import Commit
from src.model.file import File
from src.model.issue import Issue
from src.model.patch import Patch
from src.model.repo import Repo

from src.service.configService import ConfigService

class DbService: 

  def getConnection(configService):
    connection = psycopg2.connect(
      user = configService.config['datasource']['user'],
      password = configService.config['datasource']['password'],
      host = configService.config['datasource']['host'],
      port = configService.config['datasource']['port'],
      database = configService.config['datasource']['database'])
    cursor = connection.cursor()
    return cursor, connection

  def initDb(configService, cursor, connection):
    if configService.config.getboolean('datasource', 'drop-first'):
      with open(configService.config['datasource']['drop-script']) as dropScript:
        cursor.execute(dropScript.read())
        connection.commit()

    with open(configService.config['datasource']['schema']) as schema:
      cursor.execute(schema.read())
      connection.commit()

  def getLatestArchiveDate(cursor):
    selectQuery = 'select date from archive_dates order by date desc limit 1'
    cursor.execute(selectQuery)
    result = cursor.fetchone()
    if result:
      return result[0]

  def __init__(self, configService):
    self.configService = configService
    self.cursor, self.connection = DbService.getConnection(self.configService)

  def addArchiveDate(self, archiveDate, succeeded):
    insertQuery = 'insert into archive_dates(date, succeeded) ' \
      'values (%s, %s)'
    formattedDate = archiveDate.strftime(self.configService.config['date']['format'])
    self.cursor.execute(insertQuery, (formattedDate, succeeded))
    self.connection.commit()

  def addRepo(self, repo: Repo):
    insertQuery = 'insert into repositories(github_id, url, name) ' \
      'values (%s,%s,%s) returning id'
    params = (repo.github_id, repo.url, repo.name)
    return self.saveInsert(insertQuery, params, repo, lambda: self.getById(repo))

  def addIssue(self, issue: Issue):
    insertQuery = 'insert into issues(github_id, url, title, body, language, repository_id)' \
      'values (%s,%s,%s,%s,%s,%s) returning id'
    params = (issue.github_id, issue.url, issue.title, issue.body, issue.language, issue.repoId)
    return self.saveInsert(insertQuery, params, issue, lambda: self.getByIdAndUrl(issue))

  def addCommit(self, commit: Commit):
    insertQuery = 'insert into commits(github_id, url, message, language, issue_id)' \
    'values (%s,%s,%s,%s,%s) returning id'
    params = (commit.github_id, commit.url, commit.message, commit.language, commit.issueId)
    return self.saveInsert(insertQuery, params, commit)
  
  def addFile(self, file: File):
    insertQuery = 'insert into files(github_id, url, name, extension, content, hash, commit_id)' \
      'values (%s, %s, %s, %s, %s, %s, %s) returning id'
    params = (file.github_id, file.url, file.name, file.extension, file.content, file.hash, file.commitId)
    return self.saveInsert(insertQuery, params, file, lambda: self.getFileId(file))
  
  def getFileId(self, file):
    selectQuery = 'select id from %s where (github_id = %s and url = %s) or hash = %s' 

    self.cursor.execute(selectQuery, (AsIs(file.table), file.github_id, file.url, file.hash))
    return self.cursor.fetchone() 

  def addPatch(self, patch: Patch):
    insertQuery = 'insert into patches(content, file_id)' \
      'values (%s, %s) returning id'
    params = (patch.content, patch.fileId)
    return self.saveInsert(insertQuery, params, patch)

  def saveInsert(self, insertQuery, params, entity, returnExisting = None):
    try:
      self.cursor.execute(insertQuery, params)
      self.connection.commit()
      return self.cursor.fetchone()[0]
    except UniqueViolation as ex:
      self.connection.rollback()
      if returnExisting:
        return returnExisting()[0]

  def getById(self, entity):
    selectQuery = 'select id from %s where github_id = %s'  

    self.cursor.execute(selectQuery, (AsIs(entity.table), entity.github_id))
    return self.cursor.fetchone()

  def getByIdAndUrl(self, entity):
    selectQuery = 'select id from %s where github_id = %s and url = %s'  

    self.cursor.execute(selectQuery, (AsIs(entity.table), entity.github_id, entity.url))
    return self.cursor.fetchone()
