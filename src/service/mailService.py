import smtplib
import ssl
from email.message import EmailMessage

from service.configService import ConfigService

class MailService:

  def __init__(self):
    self.configService = ConfigService()
    self.mailServer = smtplib.SMTP(
      self.configService.config['mail']['host'],
      self.configService.config['mail']['port']
    )
    self.mailServer.starttls(context=ssl.create_default_context())
    self.mailServer.login(
      self.configService.config['mail']['username'],
      self.configService.config['mail']['password']
    )

  def sendMail(self, exception, archiveDate):
    msg = EmailMessage()
    msg['Subject'] = 'Error'
    msg['From'] = self.configService.config['mail']['from']
    msg['To'] = self.configService.config['mail']['to']
    msg.set_content(f'Archive Date: {str(archiveDate)} \n\nError: \n{str(exception)}')
    self.mailServer.send_message(msg)
