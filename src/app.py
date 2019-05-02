import json
import archiveClient

def validIssueEvent(jsonObj):
  if (jsonObj['type'] == 'IssuesEvent' 
    and jsonObj['payload']['action'] == 'closed' 
    and jsonObj['payload']['issue']['labels']):
    
    for label in jsonObj['payload']['issue']['labels']:
      if 'bug' in label['name'].lower():
        return True
  return False

def processIssues(jsonObj):
  if validIssueEvent(jsonObj): 
    print(jsonObj['payload']['issue']['url'])

def validPullRequest(jsonObj):
  if (jsonObj['type'] == 'PullRequestEvent'
    and jsonObj['payload']['action'] == 'closed'):
    print(jsonObj['payload']['pull_request'])

  if (jsonObj['type'] == 'PullRequestEvent' 
    and jsonObj['payload']['action'] == 'closed' 
    and jsonObj['payload']['pull_request']['labels']):
    
    for label in jsonObj['payload']['pull_request']['labels']:
      if 'bug' in label['name'].lower():
        return True
  return False

def processPullRequests(jsonObj):
  if validPullRequest(jsonObj): 
    print(jsonObj['payload']['pull_request']['url'])

def main():
  content = archiveClient.retrieveData('2018-02-01-1')
  items = []
  for line in content.splitlines():
    jsonObj = json.loads(line)
    processIssues(jsonObj)
    items.append(jsonObj)
    # processPullRequests(jsonObj)
    
  print(len(items))

if __name__== "__main__":
  main()
