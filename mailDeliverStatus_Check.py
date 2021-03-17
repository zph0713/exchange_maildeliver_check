from core import maildeliver_check,mail
from conf import settings


def main_logic():
    check_instance = maildeliver_check.MailBoxDeliverCheck()
    check_instance.threadQuery()
    message = check_instance.generatorMail()
    if message:
        mail_instance = mail.SendMail()
        mail_instance.sendMail(settings.Mail_Subject,message)
    else:
        print 'mailbox normal'


if __name__ == '__main__':
    main_logic()
