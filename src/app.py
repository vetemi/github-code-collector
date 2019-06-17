from datetime import datetime, timedelta

from src.codeCollector import CodeCollector
from src.service.mailService import MailService
from src.service.configService import ConfigService

def main():
  # oldest date 2011-02-12-0
  archiveDate = datetime(2015, 2, 12, 0)
  endDate = datetime(2015, 2, 13, 1)
  delta = timedelta(hours = 1)
  configService = ConfigService()
  codeCollector = CodeCollector(configService)
  mailService = MailService(configService)
  try:
    while archiveDate < endDate:  
      codeCollector.collectFor(archiveDate)
      archiveDate = archiveDate + delta
  except Exception as error:
    mailService.sendErrorMail(error, archiveDate)
    raise error
  
  mailService.sendSuccessMail(archiveDate, endDate)
  

if __name__== "__main__":
  main()
