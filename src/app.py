from datetime import datetime, timedelta

from codeCollector import CodeCollector

def main():
  # oldest date 2011-02-12-0
  archiveDate = datetime(2015, 2, 12, 0)
  endDate = datetime(2015, 2, 13, 1)
  delta = timedelta(hours = 1)
  codeCollector = CodeCollector()

  while archiveDate < endDate:  
    codeCollector.collectFor(archiveDate)
    archiveDate = archiveDate + delta

if __name__== "__main__":
  main()

def processPullRequests(jsonObj):
  if validPullRequest(jsonObj): 
    print(jsonObj['payload']['pull_request']['url'])

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
