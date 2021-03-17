import os,sys
BASEDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASEDIR)

LOGSDIR = os.path.join(BASEDIR,'logs')
CONFDIR = os.path.join(BASEDIR,'conf')

Config_file = os.path.join(CONFDIR,'config.ini')
Account_Info = os.path.join(CONFDIR,'account_info.yaml')

#
PARAMETERS = {'Time_Interval':1}

#Mail_Subject#
Mail_Subject = "[xxTEAM]office365 mailbox abnormal deliver status"

#Alert threshold#
Alert_Threshold = {'Deliver_Rate':15,'Fail_count':10}


#mail parameters#
MAILSET = {'Mail_Type':'plain'}#html/plain#
#mail receivers#
RECEIVERS = ['hamm_zhou@trendmicro.com.cn']
