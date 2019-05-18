from datetime import datetime, timedelta
import json

import service.archiveService
from service.githubService import GithubService

# oldest date 2011-02-12-0
archiveDate = datetime(2015, 2, 12, 0)
endDate = datetime(2015, 2, 13, 0)
delta = timedelta(hours = 1)

def process():
  while archiveDate < endDate:
    content = archiveService.retrieveData(archiveDate)
    ghService = GithubService()
    for line in content.splitlines():
      jsonObj = json.loads(line)
      if validIssueEvent(jsonObj):
        repo = dbService.addRepo(jsonObj['repo'])
        ghService.retrieveData(jsonObj['payload']['issue']['url'])

    archiveDate = archiveDate + delta

def validIssueEvent(jsonObj):
  if (jsonObj['type'] == 'IssuesEvent' 
    and jsonObj['payload']['action'] == 'closed' 
    and not isinstance(jsonObj['payload']['issue'], int)
    and jsonObj['payload']['issue']['labels']):

    for label in jsonObj['payload']['issue']['labels']:
      if 'bug' in label['name'].lower():
        return True
  return False
