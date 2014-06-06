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
    

    mail['SUBJECT']="[Miner Status P] Report " + datetime.datetime.now().strftime("%Y.%m.%d %H:%M")

    (stats,err_hosts,err_devs,err_pools)=chkstat(hosts)

    #print stats

    print len(hosts)
    print len(err_hosts)

    mail['CONTENT'] = '''<html>
                           <body>
                             <a href="https://cex.io/r/0/canaan/0/" title="CEX.IO - Trade Ghashes while they mine you Bitcoins!" target="_blank">
                              <img src="http://cex.io/informer/canaan/286ea7ed8c69fe6c98fcefeccb273fab/" width="500" height="35" border="0">
                             </a>'''
    mail['CONTENT'] += "<p>Active IP Num: " + str(len(hosts) - len(err_hosts)) + "</p>"

    mail['CONTENT'] += '''<p>
                            <table border="1">
                              <tr>
                                <th>IP</th>
                                <th>Active Dev Num</th>
                              </tr>'''
    for key in stats:
	if stats[key]<10:
	    mail['CONTENT'] += '<tr><th>' + key + "</th><th>" + str(stats[key]) + "</th></tr>"
    mail['CONTENT'] += '</table></p>' 
    #if err_devs:
#	mail['CONTENT'] += '<table border="1"><tr><th>IP</th><th>Dev #</th></tr>'
#	for e in err_devs:
#	    mail['CONTENT'] += "<tr><th>" + hosts[e[0]-1]+ "</th><th>" + str(e[1]) + "</th></tr>"
#	mail['CONTENT'] += '</table></p>'
#    else:
#	mail['CONTENT'] += "None.</p>"


#    mail['CONTENT'] += "<p>Pools:<br>"
#    if err_pools:
#        mail['CONTENT'] += '<table border="1"><tr><th>IP</th><th>Pool #</th></tr>'	
#        for e in err_pools:
#            mail['CONTENT'] += "<tr><th>" + hosts[e[0]-1]+ "</th><th>" + str(e[1]) + "</th></tr>"
#	mail['CONTENT'] += '</table></p>'
#    else:
#        mail['CONTENT'] += "None.</p>"
#
#    mail['CONTENT'] += '</body></html>'
	
    mail['CONTENT'] += '</body></html>'
    print mail['CONTENT']

    if send_mail(mail):
        print "Successed."
    else:
	print "Failed"
