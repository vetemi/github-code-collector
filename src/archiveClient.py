import requests
import gzip

baseUrl = 'https://data.gharchive.org/'

def retrieveData(date):
  response = requests.get(baseUrl + date + '.json.gz')

  if response.status_code == 200:
    return gzip.decompress(response.content)
