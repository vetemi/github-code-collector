import configparser

import mysql.connector

from service.configService import ConfigService

class DbService:

  __init__(self):
    configService = ConfigService()
    self.db = mysql.connector.connect(
      host=configService.config['Datasource']['url'],
      user=configService.config['Datasource']['user'],
      passwd=configService.config['Datasource']['password'],
      database=configService.config['Datasource']['database']
    )
    self.mycursor = mydb.cursor()
