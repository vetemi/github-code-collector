from email.message import EmailMessage
import smtplib
import ssl
import traceback

from src.service.configService import ConfigService

class MailService:

  def __init__(self, configService: ConfigService):
    self.configService = configService

  def sendErrorMail(self, exception, archiveDate, failedEvent):
    self.sendMail(
      self.createErrorMessage(exception, archiveDate, failedEvent)
    )

  def createErrorMessage(self, exception, archiveDate, failedEvent):
    msg = EmailMessage()
    msg['Subject'] = 'Github Code Collector - Error'
    msg['From'] = self.configService.config['mail']['from']
    msg['To'] = self.configService.config['mail']['to']
    msg.set_content(
      f'Archive Date: {str(archiveDate)}' \
      f'\n\nFailed Event: {str(failedEvent)}' \
      f'\n\nError: \n{traceback.format_exc()}')
    return msg

  def sendSuccessMail(self, fromDate, untilDate):
    self.sendMail(
      self.createSuccessMessage(fromDate, untilDate)
    )
  
  def createSuccessMessage(self, fromDate, untilDate):
    msg = EmailMessage()
    msg['Subject'] = 'Github Code Collector - Succeeded'
    msg['From'] = self.configService.config['mail']['from']
    msg['To'] = self.configService.config['mail']['to']
    msg.set_content(f'Everything processed from: {str(fromDate)} until: {str(untilDate)}')
    return msg

  def sendMail(self, message):
    mailServer = self.createServer()
    mailServer.send_message(message)
    mailServer.quit()

  def createServer(self):
    mailServer = smtplib.SMTP(
      self.configService.config['mail']['host'],
      self.configService.config['mail']['port']
    )
    if (self.configService.config['mail']['username'] 
      and self.configService.config['mail']['password']):

      mailServer.starttls(context=ssl.create_default_context())
      mailServer.login(
        self.configService.config['mail']['username'],
        self.configService.config['mail']['password']
      )
    return mailServer
