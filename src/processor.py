import json

import archiveClient
import githubClient

def process():
  content = archiveClient.retrieveData('2018-02-01-1')
  if (githubClient.validRateLimit())
  items = []
  for line in content.splitlines():
    jsonObj = json.loads(line)
    processIssues(jsonObj)
    items.append(jsonObj)
    # processPullRequests(jsonObj)
    
  print(len(items))

def processIssues(jsonObj):
  if validIssueEvent(jsonObj): 
    githubClient.retrieveData(jsonObj['payload']['issue']['url'])

def validIssueEvent(jsonObj):
  if (jsonObj['type'] == 'IssuesEvent' 
    and jsonObj['payload']['action'] == 'closed' 
    and jsonObj['payload']['issue']['labels']):
    
    for label in jsonObj['payload']['issue']['labels']:
      if 'bug' in label['name'].lower():
        return True
  return False
