#!/usr/bin/env python
import smtplib
from email.mime.text import MIMEText

def post(mail):

	me=mail['user']+"<"+mail['from_address']+">"
	msg = MIMEText(mail['content'],'html')
	msg['Subject'] = mail['subject']
	msg['From'] = me
	msg['To'] = mail['to_list']
	to_list = mail['to_list'].split(';')
	try:
		s = smtplib.SMTP()
		s.connect(mail['smtp_server'])
		s.login(mail['user'],mail['password'])
		s.sendmail(me, to_list, msg.as_string())
		s.close()
		return True
	except Exception, e:
		print str(e)
		return False
def sendmail(time,data,cfg):
	mail = cfg['Email'] 


	mail['user'] = mail['from_address'].split('@')[0]
	mail['subject'] = "[Miner Status " + cfg['Miner']['server_code'] + "] Report " + time

		
	mail['content'] = '''\
<html>
	<body>
		<a href="https://cex.io/r/0/canaan/0/" title="CEX.IO - Trade Ghashes while they mine you Bitcoins!" target="_blank">	
			<img src="http://cex.io/informer/canaan/286ea7ed8c69fe6c98fcefeccb273fab/" width="500" height="35" border="0">
		</a>'''
	
	alivenum = 0
	for miner in data:
		if miner[1] == "Alive":
			alivenum += 1
	mail['content'] += "\n\t\t<p>Active IP Num: " + str(alivenum) + '/' + str(len(cfg['Miner']['miner_list'])) + "</p>\n"

	mail['content'] += '''\
		<p>
		<table border="1">
			<tr>
				<th>IP</th>
				<th>Active Mod Num</th>
			</tr>'''
		
	for miner in data:
		sum_mod_num = 0
		for dev_stat in miner[4]:
			sum_mod_num += dev_stat[3]
		if sum_mod_num < int(cfg['Miner']['module_number']):
			mail['content'] += '\n\t\t\t<tr>\n\t\t\t\t<th>' + miner[0] + "</th><th>" + str(sum_mod_num) + "/" + cfg['Miner']['module_number'] + "</th>\n\t\t\t</tr>"
	mail['content'] += '\n\t\t</table>\n\t\t</p>' 
	mail['content'] += '\n\t</body>\n</html>'

	if post(mail):
		print "Successed in sending email."
	else:
		print "Failed in sending email."

if __name__ == '__main__':
	print 0
        
