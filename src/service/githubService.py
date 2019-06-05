from service.configService import ConfigService
import datetime
import json
import requests
import time

import model.commit

class GithubService:

  def __init__(self):
    self.configService = ConfigService()
    self.currentAuthIdx = 0
    
    accessTokens = []
    with open(self.configService.config['github']['access-tokens']) as f:
      accessTokens =  f.readlines()
    self.authHeaders = [self.mapAuthHeaders(i) for i in accessTokens]

  def mapAuthHeaders(self, access):
    access = access.strip()
    return {"Authorization": "Bearer " + access}

  def retrieveCommits(self, issue):
    commits = self.retrieveCommitsFromEvents(issue)

    if not commits:
      commits = self.retrieveCommitsFromPullRequest(issue)        
    return commits  

  def retrieveCommitsFromEvents(issue):
    events = self.request(issue['events_url'])
    commits = []
    if (events):
      for event in events:
        if (self.containsCommit(event) and not self.isDuplicate(event, commitUrls)):
          commit = self.request(event['commit_url'])
          if commit:
            commits.append(commit)
    return commits 

  def containsCommit(self, event):
    return event['commit_id'] and event['commit_url']
    
  def isDuplicate(self, event, commitUrls):
    for commitUrl in commitUrls:
      if event['commit_url'] == commitUrl:
        return True

    return False

  def retrieveCommitsFromPullRequest(issue):
    
    query = 'query {'
      + f'repository(owner: "{repoOwner}", name: "{repoName}") {{'
        + f'issue(number: {issueNumber}) {{'
          + 'timelineItems(first: 50) {'
            + 'nodes {'
              + '... on CrossReferencedEvent {'
                + 'source {'
                  + '... on PullRequest {'
                    + 'number'
                  + '}'
                + '}'
              + '}'
            + '}'
          + '}'
        + '}'
      + '}'
    + '}'

  def request(self, url):
    response = requests.get(url, headers=self.authHeaders[self.currentAuthIdx])
    if response.status_code == 200:
      return response.json()
    if response.status_code == 403:
      if self.currentAuthIdx == self.authHeaders.count - 1:
        # Need to sleep because all access tokens exceeded rate limits
        time.sleep(self.calculateSleepTime())
        self.currentAuthIdx = 0
      else:
        self.currentAuthIdx += 1  
      return self.request(url)
    return None

  def calculateSleepTime(self):
    response = requests.get(self.configService.config['github']['rate-limit-url']).json()
    remaining = response['rate']['remaining']

    if remaining > 0:
      return 0
    else:
      resetDate = datetime.datetime.fromtimestamp(response['rate']['reset'])
      now = datetime.datetime.now()
      return int((resetDate - now).total_seconds()) + 5
