import configparser

from pathlib import Path

class ConfigService:

  appIni = 'resources/application.ini'
  appDefaultIni = 'resources/application.ini'
  
  __init__(self):
    self.config = configparser.ConfigParser()
    if Path(appIni).is_file():
      self.config.read(appIni)
    else:
      self.config.read(appDefaultIni)
