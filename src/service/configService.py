import configparser

import os.path

class ConfigService:

  appIni = 'resources/application.ini'
  appDefaultIni = 'resources/application-default.ini'
  
  def __init__(self):
    self.config = configparser.ConfigParser()
    if os.path.exists(ConfigService.appIni):
      self.config.read(ConfigService.appIni)
    else:
      self.config.read(ConfigService.appDefaultIni)
