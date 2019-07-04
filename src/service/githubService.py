import datetime
import json
import requests
import time

from src.model.repo import Repo

from src.error.InvalidTokenError import InvalidTokenError

from src.service.configService import ConfigService
from src.service.mailService import MailService

class GithubService:

  def __init__(self, configService: ConfigService, accessToken):
    self.configService = configService
    self.authHeader = {'Authorization': f'Bearer {accessToken.strip()}'}
    self.baseUrl = self.configService.config['github']['api-repos-url']
    self.failed = False

  def retrieveIssue(self, repo: Repo, issueNumber):
    if repo and repo.name:
      return self.get(f'{self.baseUrl}/{repo.name}/issues/{issueNumber}')

  def retrieveCommits(self, issue, repo: Repo):
    commits = self.retrieveCommitsFromEvents(issue)
    if not commits and repo:
      commits = self.retrieveCommitsFromPullRequest(issue, repo)

    return commits

  def retrieveCommitsFromEvents(self, issue):
    commits = []
    if 'events_url' in issue: 
      events = self.get(issue['events_url'])
      if events:
        for event in events:
          if (self.containsCommit(event) and not self.isDuplicate(event, commits)):
            commit = self.get(event['commit_url'])
            if commit:
              commits.append(commit)
    return commits 

  def containsCommit(self, event):
    return event['commit_id'] and event['commit_url']
    
  def isDuplicate(self, event, commits):
    for commit in commits:
      if event['commit_id'] == commit['sha']:
        return True

    return False

  def retrieveCommitsFromPullRequest(self, issue, repo: Repo):
    response = self.post(
      self.configService.config['github']['graphql-url'],
      self.createQuery(issue, repo))
    
    commits = []
    if response and 'errors' not in response:
      commitSHAs = self.extractCommitSHAs(response)
      if commitSHAs:
        for commitSHA in commitSHAs:
          # This is necessary because it's not possible to retrieve the actual patches with GraphQL API
          commit = self.get(f'{self.baseUrl}/{repo.name}/commits/{commitSHA}')

          if commit:
            commits.append(commit)
    return commits

  def createQuery(self, issue, repo: Repo):
    repoOwnerName = repo.name.split('/')
    query = 'query {' \
      f'repository(owner: "{repoOwnerName[0]}", name: "{repoOwnerName[1]}") {{' \
        f'issue(number: {issue["number"]}) {{' \
          'timelineItems(first: 100, itemTypes: CROSS_REFERENCED_EVENT) {' \
            'nodes {' \
              '... on CrossReferencedEvent {' \
                'source {' \
                  '... on PullRequest {' \
                    'state ' \
                    'commits(first:100) {' \
                      'nodes {' \
                        'commit {' \
                          'oid' \
                        '}' \
                      '}' \
                    '}' \
                  '}' \
                '}' \
              '}' \
            '}' \
          '}' \
        '}' \
      '}' \
    '}'
    return json.dumps({'query': query}) 

  def extractCommitSHAs(self, response):
    commitSHAs = []
    pullRequests = response['data']['repository']['issue']['timelineItems']['nodes']
    if pullRequests:
      for pullRequest in pullRequests:
        if ('commits' in pullRequest['source'] 
          and 'state' in pullRequest['source']
          and pullRequest['source']['state'] == 'MERGED'):
          if pullRequest['source']['commits']['nodes']:
            for commit in pullRequest['source']['commits']['nodes']:
              commitSHAs.append(commit['commit']['oid'])
    return commitSHAs

  def get(self, url, contentOnly = False):
    try:
      response = requests.get(url=url, headers=self.authHeader)
    except (requests.exceptions.ConnectionError, ConnectionRefusedError):
      self.handleConnectionError()
      response = requests.get(url=url, headers=self.authHeader)
    
    return self.respond(response, lambda: self.get(url), contentOnly)
    
  def post(self, url, body, contentOnly = False):
    try:
      response = requests.post(
        url=url, headers=self.authHeader, data=body)
    except (requests.exceptions.ConnectionError, ConnectionRefusedError):
      self.handleConnectionError()
      response = requests.post(
        url=url, headers=self.authHeader, data=body)

    return self.respond(response, lambda: self.post(url, body), contentOnly)

  def handleConnectionError(self):
    if self.failed:
      raise InvalidTokenError(f'Connection refused multiple times: {self.authHeader}')
    self.failed = True
    time.sleep(61)
    
  def respond(self, response, httpRequest, contentOnly = False):
    if response.status_code == 200:
      return self.successResponse(response, contentOnly)
    if response.status_code == 403:
      return self.authFailedResponse(response, httpRequest)
    self.failed = False

  def successResponse(self, response, contentOnly = False):
    self.failed = False
    if contentOnly:
      return response.content.decode('utf-8', 'ignore')

    try:
      return response.json()
    except ValueError as e:
      return response.content.decode('utf-8', 'ignore')

  def authFailedResponse(self, response, httpRequest):
    if not self.unavailableReason(response):  
      if self.failed:
        print(f'Response of multiple failing requests: {response.content} and {response.url}')
        raise InvalidTokenError(f'Token with Header is failing multiple times: {self.authHeader}')

      self.failed = True
      sleepTime = self.calculateSleepTime(response)
      print(f'Need to sleep {sleepTime} s')
      time.sleep(sleepTime)
      return httpRequest()

  def unavailableReason(self, response):
    try:
      body = response.json()
      if 'block' in body:
        return body['block']['reason'] == 'unavailable' or body['block']['reason'] == 'tos'
    except ValueError as e:
      return False

  def calculateSleepTime(self, response):
    if 'Retry-After' in response.headers:
      waitTime = response.headers['Retry-After']
      print(f'Retry-After is set to: {waitTime}')
      if waitTime and waitTime > 0:
        return waitTime + 5

    response = requests.get(
        url=self.configService.config['github']['rate-limit-url'], 
        headers=self.authHeader).json()
    remaining = response['rate']['remaining']

    if remaining > 0:
      return 0
    else:
      resetDate = datetime.datetime.fromtimestamp(response['rate']['reset'])
      now = datetime.datetime.now()
      return int((resetDate - now).total_seconds()) + 5
