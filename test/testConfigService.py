import configparser

import os.path

class TestConfigService:

  appTestIni = 'resources/application-test.ini'
  
  def __init__(self):
    self.config = configparser.ConfigParser()
    if os.path.exists(TestConfigService.appTestIni):
      self.config.read(TestConfigService.appTestIni)
    else:
      raise Exception('No test configuration provided')
