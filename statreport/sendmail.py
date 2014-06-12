#!/usr/bin/env python
import smtplib
import uuid
from email.mime.multipart import MIMEMultipart
from email.mime.text      import MIMEText
from email.mime.image     import MIMEImage
import os
from django.template import loader, Context
from django.conf import settings

def post(mail,template_var):
	me=mail['user']+"<"+mail['from_address']+">"
	msg = MIMEMultipart('related')
	msg['Subject'] = mail['subject']
	msg['From'] = me
	msg['To'] = mail['to_list']
	to_list = mail['to_list'].split(';')
	msg_alternative = MIMEMultipart('alternative')
	msg.attach(msg_alternative)

	if 'img' in mail:
		img = dict(path=mail['img_dir'] + mail['img'], cid=str(uuid.uuid4()))

		with open(img['path'], 'rb') as file:
			msg_image = MIMEImage(file.read(), name=os.path.basename(img['path']))
			msg.attach(msg_image)
		template_var['img_cid'] = img['cid']
		msg_image.add_header('Content-ID', '<{}>'.format(img['cid']))
	tmp = mail['template'].split('/')
	template_dir = '/'.join(tmp[:-1])
	settings.configure(TEMPLATE_DIRS = (template_dir if template_dir else './'))
	t = loader.get_template(tmp[-1])
	c = Context(template_var)
	mail['content'] = t.render(c)
	msg_html = MIMEText(mail['content'],'HTML')
	msg_alternative.attach(msg_html)
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

	template_var={}
	template_var['server_code'] = cfg['Miner']['server_code']
	template_var['time'] = time
	alivenum = 0
	for miner in data:
		if miner[1] == "Alive":
			alivenum += 1
	template_var['active_ip_num'] = str(alivenum) + '/' + str(len(cfg['Miner']['miner_list']))

	template_var['err_miner_list']=[]
	for miner in data:
		sum_mod_num = 0
		for dev_stat in miner[4]:
			sum_mod_num += int(dev_stat[3])
		if sum_mod_num < int(cfg['Miner']['module_number']):
			template_var['err_miner_list'].append({ 'ip' : miner[0] , 'err_mod_num' : str(sum_mod_num) + "/" + cfg['Miner']['module_number'] })
	if 'img' in mail:
		template_var['img'] = True
	if post(mail,template_var):
		print "Successed in sending email."
	else:
		print "Failed in sending email."

if __name__ == '__main__':
	print 0

