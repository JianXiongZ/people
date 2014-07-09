#!/usr/bin/env python
from __future__ import print_function
import os
import sys
import shutil
from django.template import loader, Context
from django.conf import settings

def renderpage(time,data,cfg):

	template_var={}

	print("Rendering web page" + ' ...',end="")
	sys.stdout.flush()
	template_var['time'] = time.strftime("%Y.%m.%d %H:%M")

	alivenum = 0
	for miner in data:
		if miner[1] == "Alive":
			alivenum += 1
	template_var['active_ip_num'] = str(alivenum) + '/' + str(len(cfg['miner_list']))

	template_var['err_miner_list']=[]
	for miner in data:
		if miner[7] != '0':
			error = int(miner[7])
			error_r = []
			if error|8 == error:
				error_r.append({'msg':'Unable to connect.', 'color':'black'})
			if error|4 == error:
				error_r.append({'msg':'Alive module number too low.', 'color':'blue'})
			if error|2 == error:
				error_r.append({'msg':'Temperature 255.', 'color':'purple'})
			if error|1 == error:
				error_r.append({'msg':'Overheating.', 'color':'red'})
			template_var['err_miner_list'].append({'ip':miner[0], 'error':error_r})

	sum_mod_num = 0
	for miner in data:
		for dev_stat in miner[4]:
			sum_mod_num += int(dev_stat[3])
	sum_mod_num0 = 0
	for mod_num in cfg['mod_num_list']:
		sum_mod_num0 += int(mod_num)
	template_var['alive_mod_num'] = str(sum_mod_num) + '/' + str(sum_mod_num0)

	tmp = cfg['Webpage']['template'].split('/')
	template_dir = '/'.join(tmp[:-1])

	settings.configure(TEMPLATE_DIRS = (template_dir if template_dir else './'))
	t = loader.get_template(tmp[-1])
	c = Context(template_var)

	try:
		shutil.copyfile(cfg['TMplot']['img_dir'] + "tm-"+time.strftime("%Y_%m_%d_%H_%M")+".png", cfg['Webpage']['tm_pic'])
		shutil.copyfile(cfg['HSplot']['img_dir'] + "hs-"+time.strftime("%Y_%m_%d_%H_%M")+".png", cfg['Webpage']['hs_pic'])
		index_html = open(cfg['Webpage']['index_html'], 'w')
		index_html.write(t.render(c))
		index_html.close()
		print('Done.')
	except Exception,e:
		print(str(e))
		print('Failed.')

