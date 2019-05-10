import requests
import json

auth = {"Authorization": "Bearer 6cb9511509c0aa3c08518427e7955e84bebc6c92"}

def validRateLimit():
  response = requests.get('https://api.github.com/rate_limit', headers=auth)


def retrieveData(issueUrl):
  issue = request(issueUrl)
  if issue and issue['events_url']:
    events = request(issue['events_url'])

    commits = []
    for event in events:
      if containsCommit(event):
        commits.append(event['commit_url'])

    print(issueUrl)
    print(len(commits))

def request(url):
  response = requests.get(url, headers=auth)
  if response.status_code == 200:
    return response.json()

def containsCommit(event):
  return event['commit_id'] and event['commit_url']
