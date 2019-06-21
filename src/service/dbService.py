import psycopg2
from psycopg2.extensions import AsIs
from psycopg2.errors import UniqueViolation

from src.model.commit import Commit
from src.model.file import File
from src.model.issue import Issue
from src.model.patch import Patch
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
    return self.saveInsert(insertQuery, params, repo, lambda: self.getId(repo))

  def addIssue(self, issue: Issue):
    insertQuery = 'insert into issues(github_id, url, title, body, language, repository_id)' \
      'values (%s,%s,%s,%s,%s,%s) returning id'
    params = (issue.github_id, issue.url, issue.title, issue.body, issue.language, issue.repoId)
    print('----------------------------------')
    print(issue.github_id)
    print('........')
    print(issue.url)
    print('........')
    print(issue.title[:20])
    print('........')
    print(issue.body[:20])
    print('........')
    print(issue.language)
    print('........')
    print(issue.repoId)
    return self.saveInsert(insertQuery, params, issue, lambda: self.getId(issue))

  def getId(self, entity):
    selectQuery = 'select id from %s where github_id = %s and url = %s'  

    self.cursor.execute(selectQuery, (AsIs(entity.table), entity.github_id, entity.url))
    return self.cursor.fetchone()

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
