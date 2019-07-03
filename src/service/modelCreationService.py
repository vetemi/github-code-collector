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

class ModelCreationService:

  def createRepo(self, githubRepo):
    return Repo(
      url = githubRepo['url'],
      github_id = githubRepo['id'],
      name = githubRepo['name']) 

  def createIssue(self, githubIssue, repoId):
    lang = self.detectLang(githubIssue['body'])
    return Issue(url = githubIssue['url'],
      github_id = githubIssue['id'],
      title = githubIssue['title'],
      body = githubIssue['body'],
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
    filename, fileExtension = os.path.splitext(githubFile['filename'])
    content = self.retrieveFile(githubFile['raw_url'])
    hash = mmh3.hash128(content, signed = True)
    return File(url = githubFile['raw_url'],
      github_id = githubFile['sha'],
      name = filename,
      extension = fileExtension,
      content = content,
      hash = hash,
      commitId = commitId)

  def retrieveFile(self, url):
    try:
      return requests.get(url).content.decode('utf-8', 'ignore')
    except requests.exceptions.ConnectionError:
      time.sleep(2)
      return requests.get(url).content.decode('utf-8', 'ignore')
