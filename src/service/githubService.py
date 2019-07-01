import datetime
import json
import requests
import time

from src.service.configService import ConfigService

class GithubService:

  def __init__(self, configService: ConfigService, accessToken):
    self.configService = configService
    self.authHeader = {'Authorization': f'Bearer {accessToken.strip()}'}
    self.failed = False

  def retrieveCommits(self, issue, repo):
    commits = self.retrieveCommitsFromEvents(issue)
    if not commits:
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

  def retrieveCommitsFromPullRequest(self, issue, repo):
    response = self.post(
      self.configService.config['github']['graphql-url'],
      self.createQuery(issue, repo))
    
    commits = []
    if response and 'errors' not in response:
      commitSHAs = self.extractCommitSHAs(response)
      if commitSHAs:
        for commitSHA in commitSHAs:
          # This is necessary because it's not possible to retrieve the actual patches with GraphQL API
          baseUrl = self.configService.config['github']['api-repos-url']
          commit = self.get(f'{baseUrl}/{repo["name"]}/commits/{commitSHA}')

          if commit:
            commits.append(commit)
    return commits

  def createQuery(self, issue, repo):
    repoOwnerName = repo['name'].split('/')
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

  def get(self, url):
    response = requests.get(url=url, headers=self.authHeader)
    return self.respond(response, lambda: self.get(url))
  
  def post(self, url, body):
    response = requests.post(
      url=url, headers=self.authHeader, data=body)
    return self.respond(response, lambda: self.post(url, body))
    
  def respond(self, response, httpRequest):
    if response.status_code == 200:
      self.failed = False
      try:
        return response.json()
      except ValueError as e:
        return response.content
    if response.status_code == 403:
      if self.failed:
        raise Exception(f'failing multiple times {self.authHeader}')
      # Need to sleep because access token exceeded rate limit
      self.failed = True
      time.sleep(self.calculateSleepTime())
      return httpRequest()
    return None

  def calculateSleepTime(self):
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
