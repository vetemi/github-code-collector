import concurrent.futures
from datetime import datetime, timedelta
import time
import traceback

from src.error.collectionError import CollectionError
from src.error.InvalidTokenError import InvalidTokenError

from src.codeCollector import CodeCollector
from src.service.dbService import DbService
from src.service.mailService import MailService
from src.service.configService import ConfigService

configService = ConfigService()

def initDb(configService):
  cursor, connection = DbService.getConnection(configService)
  DbService.initDb(configService, cursor, connection)
  DbService.deleteFailedArchiveDates(cursor, connection)
  return cursor

def execute(archiveDate, deltaSteps, token, mailService):
  try:
    codeCollector = CodeCollector(configService, token)
    delta = timedelta(hours = deltaSteps)
    print(f'Thread with token started: {token}') 
    while archiveDate < datetime.now():  
      codeCollector.processFor(archiveDate)
      archiveDate = archiveDate + delta
  except Exception as error:
    print(f'Thread Error: {token}')
    print(traceback.format_exc())
    mailService.sendErrorMail(
      CollectionError(
        token = token,
        error = error,
        event = codeCollector.failedEvent,
        archiveDate = archiveDate))
    raise error

def main():
  cursor = initDb(configService)
  startDate = datetime(2011, 2, 12, 0)
  mailService = MailService(configService)
  accessTokens = []
  with open(configService.config['github']['access-tokens']) as f:
    accessTokens = f.readlines()
    
  with concurrent.futures.ThreadPoolExecutor(max_workers=len(accessTokens)) as executor:
    futures = [executor.submit(execute, startDate + timedelta(hours = idx), len(accessTokens), token, mailService) 
      for idx, token in enumerate(accessTokens)]
    for future in concurrent.futures.as_completed(futures):
      future.result()        

  mailService.sendSuccessMail(startDate, datetime.now())

if __name__== "__main__":
  main()
