import configparser

import os.path

class TestConfigService:

  appTestIni = 'resources/application-test.ini'
  
  def __init__(self):
    self.config = configparser.ConfigParser()
    if os.path.exists(ConfigService.appTestIni):
      self.config.read(ConfigService.appTestIni)
    else:
      raise Exception('No test configuration provided')
