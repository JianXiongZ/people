#!/usr/bin/env python
import smtplib
from email.mime.text import MIMEText

mailto_list=["archang@0xf8.com"]

mail_host="smtp.163.com"
mail_user="avalon_build"
mail_pass="canaan-creative"
mail_postfix="163.com"

def send_mail(mail):

    me=mail['MAIL_USER']+"<"+mail['FROM_EMAIL_ADDRESS']+">"
    msg = MIMEText(mail['CONTENT'],'html')
    msg['Subject'] = mail['SUBJECT']
    msg['From'] = me
    msg['To'] = mail['TO_EMAIL_LIST']
    to_list = mail['TO_EMAIL_LIST'].split(';')
    try:
        s = smtplib.SMTP()
        s.connect(mail['SMTP_ADDRESS'])
        s.login(mail['MAIL_USER'],mail['EMAIL_ACCOUNT_PASSWORD'])
        s.sendmail(me, to_list, msg.as_string())
        s.close()
        return True
    except Exception, e:
        print str(e)
        return False

if __name__ == '__main__':
    f = open('email.conf', 'r')
    lines = f.read().split('\n')
    mail={}
    for line in lines:
	tmp = line.split('=')
	mail[tmp[0]] = tmp[1]
    mail['MAIL_USER']=mail['FROM_EMAIL_ADDRESS'].split('@')[0]
    
    mail['SUBJECT']="Miner Stat Report Test"
    mail['CONTENT']="TestTestTestTestTestTest"
    
    print mail
    if send_mail(mail):
        print "Successed"
    else:
        print "Failed"
        
