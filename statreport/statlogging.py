#!/usr/bin/env python
from xml.dom.minidom import parse
import xml.dom.minidom
import datetime
import os

def writelog(data,logdir,filename):
	## write XML log file
	print 'Logging into ' + logdir + filename + '... ',
	log = '<?xml version="1.0"?>\n'
	time = filename.strip("log-").strip(".xml")
	log += "<data>\n\t<time>" + time + "</time>\n"
	for miner in data:
		log += "\t<miner>\n"
		log += "\t\t<IP>" + miner[0] + "</IP>\n"
		for dev_stat in miner[1]:
			log += "\t\t<dev>\n"
			log += "\t\t\t<DeviceElapsed>" + dev_stat[0] + "</DeviceElapsed>\n"
			log += "\t\t\t<TotalMH>" + dev_stat[1] + "</TotalMH>\n"
			log += "\t\t\t<MaxTemperature>" + dev_stat[2] + "</MaxTemperature>\n"
			log += "\t\t\t<ModuleNumber>" + str(dev_stat[3]) + "</ModuleNumber>\n"
			for temp in dev_stat[4]:
				log += "\t\t\t<Temperature>" + temp + "</Temperature>\n"
			for fan in dev_stat[5]:
				log += "\t\t\t<FanSpeed>" + fan + "</FanSpeed>\n"
			log += "\t\t</dev>\n"
		for pool_stat in miner[2]:
			log += "\t\t<pool>\n"
			log += "\t\t\t<URL>" + pool_stat[0] + "</URL>\n"
			log += "\t\t\t<Status>" + pool_stat[1] + "</Status>\n"
			log += "\t\t</pool>\n"
		log += "\t</miner>\n"
	log += "</data>"
	
	try:
		logfile = open(logdir + filename, 'w')
	except IOError:
		os.makedirs(logdir)
		logfile = open(logdir + filename, 'w')
	logfile.write(log)
	logfile.close()
	print 'Done.'

def readlog(logdir,filename):
	## read XML log file
	data=[]
	DOMTree = xml.dom.minidom.parse( logdir + filename )
	log = DOMTree.documentElement
	time = datetime.datetime.strptime(log.getElementsByTagName("time")[0].childNodes[0].data,"%Y_%m_%d_%H_%M")
	for minerXML in log.getElementsByTagName("miner"):
		miner=[]
		dev=[]
		pool=[]
		miner.append(minerXML.getElementsByTagName("IP")[0].childNodes[0].data)
		for dev_statXML in minerXML.getElementsByTagName("dev"):
			dev_stat=[]
			dev_stat.append(dev_statXML.getElementsByTagName("DeviceElapsed")[0].childNodes[0].data)
			dev_stat.append(dev_statXML.getElementsByTagName("TotalMH")[0].childNodes[0].data)
			dev_stat.append(dev_statXML.getElementsByTagName("MaxTemperature")[0].childNodes[0].data)
			dev_stat.append(dev_statXML.getElementsByTagName("ModuleNumber")[0].childNodes[0].data)
			temp=[]
			for tempXML in dev_statXML.getElementsByTagName("Temperature"):
				temp.append(tempXML.childNodes[0].data)
			dev_stat.append(temp)
			fan=[]
			for fanXML in dev_statXML.getElementsByTagName("FanSpeed"):
				fan.append(fanXML.childNodes[0].data)
			dev_stat.append(fan)
			dev.append(dev_stat)
		for pool_statXML in minerXML.getElementsByTagName("pool"):
			pool_stat=[]
			pool_stat.append(pool_statXML.getElementsByTagName("URL")[0].childNodes[0].data)
			pool_stat.append(pool_statXML.getElementsByTagName("Status")[0].childNodes[0].data)
			pool.append(pool_stat)
		miner.append(dev)
		miner.append(pool)
		data.append(miner)
			
	return (data,time)
	
if __name__ == '__main__':
	logdir = './log/'
	logname = 'log-example.xml'
	(data,time) = readlog(logdir,logname)
	
	for miner in data:
		print miner[0] + ':'
		i = 1
		for dev_stat in miner[1]:
			print '\tModule #' + str(i) + ':'
			print '\t\tDevice Elapsed: ' + dev_stat[0]
			print '\t\tTotal MH: ' + dev_stat[1]
			print '\t\tTemperature: ' + dev_stat[2]
			print '\t\tModules Number: ' + str(dev_stat[3])
			print '\t\tTemperature List: ' + ','.join(dev_stat[4])
			print '\t\tFan Speed List: ' + ','.join(dev_stat[5])
			i += 1
		
		i = 1
		for pool_stat in miner[2]:
			print '\tPool #' + str(i) + ':'
			print '\t\tURL: ' + pool_stat[0]
			print '\t\tStatus: ' + pool_stat[1]
			i += 1
		print "------------------------------------------------------------------------------"

