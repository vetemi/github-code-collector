import concurrent.futures
from datetime import datetime, timedelta
import time

from src.error.collectionError import CollectionError

from src.codeCollector import CodeCollector
from src.service.dbService import DbService
from src.service.mailService import MailService
from src.service.configService import ConfigService

configService = ConfigService()

def initDb(configService):
  cursor, connection = DbService.getConnection(configService)
  DbService.initDb(configService, cursor, connection)
  return cursor

def execute(archiveDate, deltaSteps, token):
  codeCollector = CodeCollector(configService, token)
  delta = timedelta(hours = deltaSteps)
  while archiveDate < datetime.now():  
    try:
      codeCollector.collectFor(archiveDate)
      archiveDate = archiveDate + delta
    except Exception as error:
      raise CollectionError(
        message = 'something went wrong',
        error = error,
        event = codeCollector.failedEvent,
        archiveDate = archiveDate)

def main():
  cursor = initDb(configService)
  startDate = datetime(2011, 2, 12, 0)
  mailService = MailService(configService)
  accessTokens = []
  with open(configService.config['github']['access-tokens']) as f:
    accessTokens = f.readlines()
    
  with concurrent.futures.ThreadPoolExecutor(max_workers=len(accessTokens)) as executor:
    futures = [executor.submit(execute, startDate + timedelta(hours = idx), len(accessTokens), token) 
      for idx, token in enumerate(accessTokens)]
    for future in concurrent.futures.as_completed(futures):
      try:
        result = future.result()
      except CollectionError as error:
        mailService.sendErrorMail(error)
        raise error        

  mailService.sendSuccessMail(startDate, endDate)

if __name__== "__main__":
  main()
