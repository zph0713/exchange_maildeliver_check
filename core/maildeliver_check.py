import os,sys,re
BASEDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASEDIR)

import datetime, time
import yaml,json
import requests
import threading
from prettytable import PrettyTable

from logger import Logger
from conf import settings


LOG = Logger('main_program')

class MailBoxDeliverCheck(object):
    def __init__(self):
        self._generatorDateTime(settings.PARAMETERS['Time_Interval'])
        self._getAccountsINFO()
        #self._url = "https://reports.office365.com/ecp/reportingwebservice/reporting.svc/MessageTrace?$select=Status,SenderAddress,RecipientAddress&$filter=StartDate%20eq%20datetime'"+ self._start_time +"'%20and%20EndDate%20eq%20datetime'"+ self._current_time +"'%20&$format=Json"

        self._MessageTrace = "https://reports.office365.com/ecp/reportingwebservice/reporting.svc/MessageTrace?" \
                             "$select=Status,SenderAddress,RecipientAddress&$filter=StartDate%20eq%20datetime'" \
                             + self._start_time + "'%20and%20EndDate%20eq%20datetime'" + self._current_time + "'%20&$format=Json"
        self._MailTrafficSummary = "https://reports.office365.com/ecp/reportingwebservice/reporting.svc/MailTrafficSummary?" \
                                   "$select=C1,C2&$filter=Category%20eq%20'TopMailSender'%20and%20     StartDate%20eq%20datetime'"\
                                   +self._day_start_time+"'%20and%20     EndDate%20eq%20datetime'"+self._current_time+"'&$top=10&$format=Json"

       # self._MessageTrace_test = "https://reports.office365.com/ecp/reportingwebservice/reporting.svc/MessageTrace?" \
        #                     "$select=Status,SenderAddress,RecipientAddress&$filter=StartDate%20eq%20datetime'{}'%20and%20EndDate%20eq%20datetime'{}'%20&$format=Json".format(start_time,current_time)



        self._thread_list = list()
        self._mailbox_status = list()
        self._mailbox_list = list()

    def _generatorDateTime(self,time_interval):
        self._current_time = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        st = datetime.datetime.now() - datetime.timedelta(hours=time_interval)
        self._start_time = st.strftime("%Y-%m-%dT%H:%M:%SZ")
        self._day_start_time = st.strftime("%Y-%m-%dT00:00:00")

    def _getAccountsINFO(self):
        with open(settings.Account_Info,'r') as f:
            self._Account = yaml.load(f)['Account_Info']

    def threadQuery(self):
        thread_list = list()
        for account in self._Account:
            thread_run = threading.Thread(target=self.queryDeliverStatus,args=(account['username'],account['password'],))
            thread_list.append(thread_run)
            thread_run.start()
        for th in thread_list:
            th.join()

    def queryDeliverStatus(self,username,password):
        response_deliver = requests.get(self._MessageTrace,auth=(username,password),headers={"content-type": "text/plain"})
        if response_deliver.status_code == 200:
            self.statisticsMailBoxStatus(username,response_deliver.json()["d"]["results"])
        else:
            print('%s mailbox not login' % username)

    def statisticsMailBoxStatus(self,account,response):
        success_list = list()
        fail_list = list()
        for res in response:
            #print res
            if 'trendmicro' in res['SenderAddress']:
                if res["Status"] == "Delivered":
                    success_list.append(res['SenderAddress'])
                elif res["Status"] == "Failed":
                    fail_list.append(res['SenderAddress'])
        for mailbox in set(success_list):
            fail_count = fail_list.count(mailbox)
            success_count = success_list.count(mailbox)
            rate_float = "%.2f%%" % (float(fail_count) / (float(success_count)+float(fail_count)) *100)

            mailtotal = fail_count + success_count
            self._mailbox_list.append(mailbox)
            
           # print(self._MessageTrace_test('aaaaa','bbbb'))
            #if fail_count >= settings.Alert_Threshold['Fail_count'] or rate_float >= "%.2f%%" % (settings.Alert_Threshold['Deliver_Rate'] * 100):
            if fail_count >= settings.Alert_Threshold['Fail_count']:
                mailbox_status = dict()
                mailbox_status['adminbox'] = account
                mailbox_status['mailbox'] = mailbox
                mailbox_status['success'] = success_count
                mailbox_status['fail'] = fail_count
                mailbox_status['rate'] = rate_float
                self._mailbox_status.append(mailbox_status)

    def recordSentnumber(self,mailcount):
        record_dict = dict()
        
            
    def generatorMail(self):
        mail_t = list()
        for res in self._mailbox_status:
            mail_template = "Mailbox : %s  Deliver_failure_count : %d  Failure_rate : %s \n" %(res['mailbox'],res['fail'],res['rate'])
            mail_t.append(mail_template)
        mail_text = '\n\n'.join(mail_t)
        return mail_text
        


if __name__ == "__main__":
    mbm = MailBlockMonitor()
    mbm.threadQuery()
    mbm.generatorMail()

