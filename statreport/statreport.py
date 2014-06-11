#!/usr/bin/env python
from sendmail import sendmail
from chkstat import chkstat
from statlogging import writelog
from hsplot import plot
from readconfig import readconfig
import datetime
import argparse
import os

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description="Generate miner status report.")
	parser.add_argument("-m","--email", help="send email", action="store_true")
	parser.add_argument("-p","--plot", help="plot hash speed graph", action="store_true")
	parser.add_argument("-c","--config", type=str, help="use another config file rather than ./statreport.conf")
	args = parser.parse_args()
	
	
	if args.config:
		cfg = readconfig(args.config)
	else:
		cfg = readconfig("./statreport.conf")
	if cfg['Log']['directory'][-1] != '/':
		cfg['Log']['directory'] += '/' 
	if cfg['Plot']['img_dir'][-1] != '/':
		cfg['Plot']['img_dir'] += '/' 
	if not os.path.isdir(cfg['Log']['directory']):
		os.makedirs(cfg['Log']['directory'])
	if not os.path.isdir(cfg['Plot']['img_dir']):
		os.makedirs(cfg['Plot']['img_dir'])
	cfg['Miner']['miner_list'] = list(filter(None, (x.strip() for x in cfg['Miner']['miner_list'].splitlines())))	
		
		
	
	time_now = datetime.datetime.now()


	data = chkstat(cfg)

	writelog(data,cfg['Log']['directory'],"log-" + time_now.strftime("%Y_%m_%d_%H_%M") + ".xml")

	if args.plot:
		png = plot(time_now,cfg)
		cfg['Email']['img_dir'] = cfg['Plot']['img_dir']
		cfg['Email']['img'] = png

	if args.email:
		sendmail(time_now.strftime("%Y-%m-%d %H:%M"),data,cfg)
		
