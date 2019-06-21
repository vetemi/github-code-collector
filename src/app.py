from datetime import datetime, timedelta
import time

from src.codeCollector import CodeCollector
from src.service.mailService import MailService
from src.service.configService import ConfigService

def main():
  # oldest date 2011-02-12-0
  start_time = time.time()
  archiveDate = datetime(2015, 2, 12, 0)
  endDate = datetime(2015, 2, 12, 1)
  delta = timedelta(hours = 1)
  configService = ConfigService()
  codeCollector = CodeCollector(configService)
  mailService = MailService(configService)

  try:
    while archiveDate < endDate:  
      codeCollector.collectFor(archiveDate)
      archiveDate = archiveDate + delta
  except Exception as error:
    mailService.sendErrorMail(
      error, 
      archiveDate, 
      codeCollector.failedEvent)
    raise error
  
  mailService.sendSuccessMail(archiveDate, endDate)
  print("--- %s seconds ---" % (time.time() - start_time))
  

if __name__== "__main__":
  main()
