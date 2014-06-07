#!/usr/bin/env python

def writelog(data,logdir,filename):
	log = '<?xml version="1.0"?>\n'
	time = filename.strip("log-").strip(".xml")
	log += "<data>\n\t<time>" + time + "</time>\n"
	for miner in data:
		log += "\t<miner>\n"
		log += "\t\t<IP>" + miner[0] + "</IP>\n"
		for dev_stat in miner[1]:
			log += "\t\t<dev>\n"
			log += "\t\t\t<Device Elapsed>" + dev_stat[0] + "</Device Elapsed>\n"
			log += "\t\t\t<Total MH>" + dev_stat[1] + "</Total MH>\n"
			log += "\t\t\t<Max Temperature>" + dev_stat[2] + "</Max Temperature>\n"
			log += "\t\t\t<Module Number>" + str(dev_stat[3]) + "</Module Number>\n"
			for temp in dev_stat[4]:
				log += "\t\t\t<Temperature>" + temp + "</Temperature>\n"
			for fan in dev_stat[5]:
				log += "\t\t\t<Fan Speed>" + fan + "</Fan Speed>\n"
			log += "\t\t</dev>\n"
		for pool_stat in miner[2]:
			log += "\t\t<pool>\n"
			log += "\t\t\t<URL>" + pool_stat[0] + "</URL>\n"
			log += "\t\t\t<Status>" + pool_stat[1] + "</Status>\n"
			log += "\t\t</pool>\n"
		log += "\t</miner>\n"
	log += "</data>"

	logfile = open(logdir + filename, 'w')
	logfile.write(log)
	logfile.close()

def readlog(logdir,filename):
	return 0
	
if __name__ == '__main__':
	i = 0
