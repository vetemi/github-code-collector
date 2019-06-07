from datetime import datetime, timedelta

from codeCollector import CodeCollector
from service.mailService import MailService

def main():
  # oldest date 2011-02-12-0
  archiveDate = datetime(2015, 2, 12, 0)
  endDate = datetime(2015, 2, 13, 1)
  delta = timedelta(hours = 1)
  codeCollector = CodeCollector()
  mailService = MailService()
  try:
    while archiveDate < endDate:  
      codeCollector.collectFor(archiveDate)
      archiveDate = archiveDate + delta
  except Exception as error:
    mailService.sendErrorMail(error, archiveDate)
  
  mailService.sendSuccessMail(archiveDate, endDate)
  

if __name__== "__main__":
  main()
