#!/usr/bin/env python
from send_mail import send_mail
from chkstat import chkstat
from statlogging import writelog
from hsplot import plot
import datetime
import argparse
import matplotlib
matplotlib.use('Agg') 

MOD_NUM_PER_MINER = 10
SERVER_CODE = 'P'
STAT_LOG_DIR = './log'

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description="Generate miner status report.")
	parser.add_argument("-m","--email", help="send email", action="store_true")
	parser.add_argument("-p","--plot", help="plot hash speed graph", action="store_true")
	args = parser.parse_args()
		
	time_now = datetime.datetime.now()
	time = time_now.strftime("%Y.%m.%d %H:%M")
	logdir = STAT_LOG_DIR if STAT_LOG_DIR[-1] == '/' else STAT_LOG_DIR + '/'
	logname = "log-" + time_now.strftime("%Y_%m_%d_%H_%M") + ".xml"


	hosts=[]
	f = open('minerlist.txt','r')
	lines = f.read().split('\n')
	for line in lines:
		if line == '':
			continue
		hosts.append(line)	

	data = chkstat(hosts)
	writelog(data,logdir,logname)

	if args.plot:
		plot(time_now,logdir)

	if args.email:
	
		f = open('email.conf', 'r')
		lines = f.read().split('\n')
		mail={}
		for line in lines:
			if line=='':
				continue
			tmp = line.split('=')
			mail[tmp[0]] = tmp[1]



		mail['MAIL_USER'] = mail['FROM_EMAIL_ADDRESS'].split('@')[0]
		mail['SUBJECT'] = "[Miner Status " + SERVER_CODE + "] Report " + time

		
		mail['CONTENT'] = '''\
<html>
	<body>
		<a href="https://cex.io/r/0/canaan/0/" title="CEX.IO - Trade Ghashes while they mine you Bitcoins!" target="_blank">	
			<img src="http://cex.io/informer/canaan/286ea7ed8c69fe6c98fcefeccb273fab/" width="500" height="35" border="0">
		</a>'''
		
		mail['CONTENT'] += "\n\t\t<p>Active IP Num: " + str(len(data)) + '/' + str(len(hosts)) + "</p>\n"

		mail['CONTENT'] += '''\
		<p>
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
				mail['CONTENT'] += '\n\t\t\t<tr>\n\t\t\t\t<th>' + miner[0] + "</th><th>" + str(sum_mod_num) + "/" + str(MOD_NUM_PER_MINER) + "</th>\n\t\t\t</tr>"
		mail['CONTENT'] += '\n\t\t</table>\n\t\t</p>' 
		mail['CONTENT'] += '\n\t</body>\n</html>'
		print mail['CONTENT']

		if send_mail(mail):
			print "Successed in sending email."
		else:
			print "Failed in sending email."
