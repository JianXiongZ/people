#!/usr/bin/env python
from send_mail import send_mail
from chkstat import chkstat
from statlogging import *
import datetime

MOD_NUM_PER_MINER = 10
SERVER_CODE = 'P'
STAT_LOG_PATH = './log'

if __name__ == '__main__':
	time_now = datetime.datetime.now()
	time = time_now.strftime("%Y.%m.%d %H:%M")
	logdir = STAT_LOG_PATH if STAT_LOG_PATH[-1] == '/' else STAT_LOG_PATH + '/'
	logname = "log-" + time_now.strftime("%Y_%m_%d_%H_%M") + ".xml"
	
	
	f = open('email.conf', 'r')
	lines = f.read().split('\n')
	mail={}
	for line in lines:
		if line=='':
			continue
		tmp = line.split('=')
		mail[tmp[0]] = tmp[1]

	hosts=[]
	f = open('minerlist.txt','r')
	lines = f.read().split('\n')
	for line in lines:
		if line == '':
			continue
		hosts.append(line)

	mail['MAIL_USER'] = mail['FROM_EMAIL_ADDRESS'].split('@')[0]
	mail['SUBJECT'] = "[Miner Status " + SERVER_CODE + "] Report " + time

	data = chkstat(hosts)
	writelog(data,logdir,logname)
	
	mail['CONTENT'] = '''<html>
							<body>
								<a href="https://cex.io/r/0/canaan/0/" title="CEX.IO - Trade Ghashes while they mine you Bitcoins!" target="_blank">	
									<img src="http://cex.io/informer/canaan/286ea7ed8c69fe6c98fcefeccb273fab/" width="500" height="35" border="0">
								</a>'''
	mail['CONTENT'] += "<p>Active IP Num: " + str(len(data)) + '/' + str(len(hosts)) + "</p>"

	mail['CONTENT'] += '''<p>
							<table border="1">
								<tr>
									<th>IP</th>
									<th>Active Mod Num</th>
								</tr>'''
	for miner in data:
		sum_mod_num = 0
		for dev_stat in miner[1]:
			sum_mod_num += dev_stat[3]
		if sum_mod_num < MOD_NUM_PER_MINER:
			mail['CONTENT'] += '<tr><th>' + miner[0] + "</th><th>" + str(sum_mod_num) + "/" + str(MOD_NUM_PER_MINER) + "</th></tr>"
	mail['CONTENT'] += '</table></p>' 
	mail['CONTENT'] += '</body></html>'
	print mail['CONTENT']

	if send_mail(mail):
		print "Successed."
	else:
		print "Failed"
