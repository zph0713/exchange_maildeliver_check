import ConfigParser
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header

from conf import settings
from logger import Logger

LOG = Logger('mailreport')


class SendMail(object):
    def __init__(self):
        self._getConfig()

    def _getConfig(self):
        config = ConfigParser.RawConfigParser()
        config.read(settings.Config_file)
        ##MailServerInfo##
        self.mail_server = config.get('mail_server','smtp_server')
        self.mail_port = config.get('mail_server','port')
        self.mail_user = config.get('mail_server','smtp_user')
        self.mail_passwd = config.get('mail_server','smtp_passwd')
        self.source_addr = config.get('mail_server','source_address')

    def sendMail(self,Subject,Message,files_list=None):
        maillog = 'send to %s' %(settings.RECEIVERS)
        LOG.info(maillog)
        if Message != None:
            message = MIMEMultipart()
            Receivers = ','
            message['From'] = self.source_addr
            message['To'] = Header(Receivers.join(settings.RECEIVERS))
            message['Subject'] = Header(Subject,'utf-8')
            message.attach(MIMEText(Message,settings.MAILSET['Mail_Type'],'utf-8'))
            if files_list != None:
                for attach in files_list:
                    att = MIMEText(open(attach,'rb').read(),'base64','utf-8')
                
                    file_name = attach.split('/')[-1]
                    att.add_header('Content-Disposition', 'attachment', filename=file_name)
                    message.attach(att)
            try:
                smtpObj = smtplib.SMTP()
                #smtpObj.set_debuglevel(1)
                smtpObj.connect(self.mail_server,self.mail_port)
                smtpObj.ehlo()
                smtpObj.starttls()
                smtpObj.login(self.mail_user,self.mail_passwd)
                smtpObj.sendmail(self.source_addr,settings.RECEIVERS,message.as_string())
                LOG.info('mail send successfull')
                smtpObj.quit()
            except smtplib.SMTPException as e:
                LOG.error(e)
        else:
            print('no data')
