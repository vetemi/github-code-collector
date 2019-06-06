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
    print('error')
    raise Exception('something')
  except Exception as e:
    mailService.sendMail(e, archiveDate)
    

if __name__== "__main__":
  main()
