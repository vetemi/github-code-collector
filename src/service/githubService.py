import datetime
import json
import requests
import time

class GithubService:

  def __init__(self):
    accessTokens = []
    with open('resources/access-tokens.txt') as f:
      accessTokens =  f.readlines()
    self.authHeaders = [self.mapAuthHeaders(i) for i in accessTokens]

  def mapAuthHeaders(self, access):
    access = access.strip()
    return {"Authorization": "Bearer " + access}

  def retrieveData(self, issueUrl):      
    issue = self.request(issueUrl)
    if issue and issue['events_url']:
      events = self.request(issue['events_url'])

      commits = []
      for event in events:
        if (self.containsCommit(event) and not self.isDuplicate(event, commits)):
          commits.append(self.request(event['commit_url']))

  def request(self, url):
    for auth in self.authHeaders:
      response = requests.get(url, headers=auth)
      if response.status_code == 200:
        return response.json()
      if response.status_code == 404:
        return None
    # Need to sleep because all access tokens exceeded rate limits
    time.sleep(60*60)
    return self.request(url)

  def containsCommit(self, event):
    return event['commit_id'] and event['commit_url']
    
  def isDuplicate(self, event, commits):
    for commit in commits:
      if event['commit_id'] == commit['sha']:
        return True

    return False
