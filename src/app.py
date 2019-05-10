
import processor

def main():
  processor.process()

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
