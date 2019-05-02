import requests

def retrieveData(issueUrl):
  issue = request(issueUrl)
  events = request(issue['events_url'])

  for event in events:
    if 

  
    return gzip.decompress(response.content)

def request(url):
  response = requests.get(url)

  if response.status_code == 200:
    return response.content
