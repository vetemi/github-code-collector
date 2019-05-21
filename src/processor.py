from service.archiveService import ArchiveService
from datetime import datetime, timedelta
from service.dbService import DbService
import json
from service.githubService import GithubService

def process():
  archiveService = ArchiveService()
  ghService = GithubService()
  dbService = DbService()
  
  # oldest date 2011-02-12-0
  archiveDate = datetime(2015, 2, 12, 0)
  endDate = datetime(2015, 2, 13, 0)
  delta = timedelta(hours = 1)

  while archiveDate < endDate:
    content = archiveService.retrieveData(archiveDate)
    for line in content.splitlines():
      jsonObj = json.loads(line)
      if validIssueEvent(jsonObj):
        print(jsonObj)
        ghService.retrieveData(jsonObj)

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
