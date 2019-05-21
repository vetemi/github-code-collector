import configparser

from pathlib import Path

class ConfigService:

  appIni = '/resources/application.ini'
  appDefaultIni = 'resources/application-default.ini'
  
  def __init__(self):
    self.config = configparser.ConfigParser()
    if Path(ConfigService.appIni).is_file():
      self.config.read(ConfigService.appIni)
    else:
      self.config.read(ConfigService.appDefaultIni)
