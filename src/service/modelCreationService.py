import requests
import os
import time

import mmh3
import langdetect

from src.model.commit import Commit
from src.model.file import File
from src.model.issue import Issue
from src.model.patch import Patch
from src.model.repo import Repo

from src.service.githubService import GithubService

class ModelCreationService:

  def __init__(self, githubService: GithubService):
    self.githubService = githubService

  def createRepo(self, event):
    repo = self.retrieveRepoFrom(event)
    if repo:
      repoId = None
      if 'id' in repo:
        repoId = repo['id']

      repoName = self.extractRepoName(repo)
      return Repo(
        url = repo['url'],
        github_id = repoId,
        name = repoName) 

  def retrieveRepoFrom(self, event):
    if 'repo' in event:
      return event['repo']
    elif 'repository' in event:
      return event['repository']

  def extractRepoName(self, repo):
    return (repo['name'] if '/' in repo['name'] 
      else f'{repo["owner"]}/{repo["name"]}')

  def createIssue(self, githubIssue, repoId):
    lang = self.detectLang(githubIssue['body'])
    return Issue(url = githubIssue['url'],
      github_id = githubIssue['id'],
      title = self.removeNullLiterals(githubIssue['title']),
      body = self.removeNullLiterals(githubIssue['body']),
      labeled = True if githubIssue['labels'] else False,
      language = lang,
      repoId = repoId)

  def createCommit(self, githubCommit, issueId):
    lang = self.detectLang(githubCommit['commit']['message'])
    return Commit(url = githubCommit['url'],
      github_id = githubCommit['sha'],
      message = githubCommit['commit']['message'],
      language = lang,
      issueId = issueId)

  def detectLang(self, text):
    if text:
      try:
        return langdetect.detect(text) 
      except:
        pass

  def createFile(self, githubFile, commitId):
    content = self.githubService.get(url = githubFile['raw_url'], contentOnly = True)
    if content:
      filename, fileExtension = os.path.splitext(githubFile['filename'])
      hash = mmh3.hash128(content, signed = True)
      return File(url = githubFile['raw_url'],
        github_id = githubFile['sha'],
        name = filename,
        extension = fileExtension,
        content = self.removeNullLiterals(content),
        hash = hash,
        commitId = commitId)

  def removeNullLiterals(self, text):
    return text.replace('\x00', '').replace('\00', '').replace('\0', '')
