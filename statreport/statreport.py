#!/usr/bin/env python
from send_mail import send_mail
from chkstat import chkstat
import datetime

if __name__ == '__main__':
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

    mail['MAIL_USER']=mail['FROM_EMAIL_ADDRESS'].split('@')[0]
    

    mail['SUBJECT']="Miner Stat Report " + datetime.datetime.now().strftime("%Y.%m.%d %H:%M")

    (err_devs,err_pools)=chkstat(hosts)

    mail['CONTENT'] = "<html><body>Err List:<p>Devs:<br>"
    if err_devs:
	mail['CONTENT'] += '<table border="1"><tr><th>IP</th><th>Dev #</th></tr>'
	for e in err_devs:
	    mail['CONTENT'] += "<tr><th>" + hosts[e[0]-1]+ "</th><th>" + str(e[1]) + "</th></tr>"
	mail['CONTENT'] += '</table></p>'
    else:
	mail['CONTENT'] += "None.</p>"


    mail['CONTENT'] += "<p>Pools:<br>"
    if err_pools:
        mail['CONTENT'] += '<table border="1"><tr><th>IP</th><th>Pool #</th></tr>'	
        for e in err_pools:
            mail['CONTENT'] += "<tr><th>" + hosts[e[0]-1]+ "</th><th>" + str(e[1]) + "</th></tr>"
	mail['CONTENT'] += '</table></p>'
    else:
        mail['CONTENT'] += "None.</p>"

    mail['CONTENT'] += '</body></html>'
	
    
    print mail['CONTENT']

    if send_mail(mail):
        print "Successed."
    else:
	print "Failed"
