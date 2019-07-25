from src.service.configService import ConfigService
from gzip import GzipFile
from io import BytesIO
import requests

class ArchiveService:

  def __init__(self, configService: ConfigService):
    self.baseUrl = configService.config['github']['archive-url']

  def retrieveData(self, date):
    response = requests.get(self.baseUrl + date.strftime('%Y-%m-%d-%-H') + '.json.gz')
    if response.status_code == 200:
      return GzipFile(fileobj=BytesIO(response.content))
