from service.configService import ConfigService
import datetime
import json
import requests
import time

import model.commit

class GithubService:

  def __init__(self):
    configService = ConfigService()
    accessTokens = []
    with open(configService.config['Github']['access-tokens']) as f:
      accessTokens =  f.readlines()
    self.authHeaders = [self.mapAuthHeaders(i) for i in accessTokens]

  def mapAuthHeaders(self, access):
    access = access.strip()
    return {"Authorization": "Bearer " + access}

  def retrieveData(self, issueEvent):       
    issue = self.request(jsonObj['payload']['issue']['url'])
    if issue and issue['events_url']:
      events = self.request(issue['events_url'])

      commits = []
      for event in events:
        if (self.containsCommit(event) and not self.isDuplicate(event, commits)):
          print(event['commit_url'])

      # if commits.count != 0:
      #   return createData(jsonObj['repo'], commits )

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
