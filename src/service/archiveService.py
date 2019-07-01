from src.service.configService import ConfigService
import gzip
import requests

class ArchiveService:

  def __init__(self, configService: ConfigService):
    self.baseUrl = configService.config['github']['archive-url']
    self.dateFormat = configService.config['date']['format']

  def retrieveData(self, date):
    response = requests.get(self.baseUrl + date.strftime(self.dateFormat) + '.json.gz')
    if response.status_code == 200:
      return gzip.decompress(response.content)
