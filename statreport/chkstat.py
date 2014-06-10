#!/usr/bin/env python
import telnetlib
import re
import time
from readconfig import readconfig

def chkstat(cfg):

	elapsed_time_flag	= re.compile('Device Elapsed=(.*)$')
	total_Mh_flag		= re.compile('Total MH=([^,]*),')
	temperature_d_flag	= re.compile('Temperature=([^,]*),')
	module_id_flag		= re.compile('ID\d MM Version')
	temperature_s_flag	= re.compile('Temperature(\d=[^,]*),')
	fan_flag			= re.compile('Fan(\d=[^,]*),')
	pool_url_flag		= re.compile('URL=([^,]*),')
	pool_alive_flag		= re.compile('Status=([^,]*),')
	
	#ignore pool stat in ' -o stats'
	stat_pool_flag		= re.compile('ID=POOL')
	
	data = []
    
	i = 0
	time_out = []
	while i < len(cfg['Miner']['miner_list']):
		h = cfg['Miner']['miner_list'][i]

		if len(time_out) < i+1:
			time_out.append(1)
		else:
			time_out[i] += 1
			
		miner = []
		
		tn = telnetlib.Telnet()

		err_conn_flag = False
		for k in range(0,int(cfg['Telnet']['retry'])):
			##try connecting for some times
			try:
				print 'Conneting ' + h +' ...',
				tn.open(h,23,int(time_out[i]))
				print 'Done.'
				break
			except:
				tn.close()
				print 'Error' + ('. Try Again.' if k < int(cfg['Telnet']['retry'])-1 else '. Skip.')
				err_conn_flag = True
		if err_conn_flag:
			miner.append(h)
			miner.append('Dead')
			miner.append('0')
			miner.append('0')
			miner.append([])
			miner.append([])
			data.append(miner)
			i += 1
			continue
		
		try:
			## read summary ##
			tn.write('cgminer-api -o summary\n')
		
			## read devs ##
			tn.write('cgminer-api -o devs\n')
		
			## read stats ##
			tn.write('cgminer-api -o stats\n')

			## read pools ##
			tn.write('cgminer-api -o pools\n')

			tn.write('exit\n')

			tmp = tn.read_all().split('cgminer-api')
			
		except:
			tn.close()
			print "Connection lost. Use larger time-out number and try again."
			continue
		
		tn.close()

		##!!!!!!!!! Bug Warning:
		##!!!!!!!!! Condition: Some dev gets down between running 'cgminer-api -o devs' & '... -o stats'
		##!!!!!!!!! Result: Different dev num in dev_data & stat_data
		summary = tmp[-4]
		dev_data = tmp[-3]
		stat_data = tmp[-2]
		pool_data = tmp[-1]


		##ToDo: close this loop and create a new one. 

		dev = []
		pool = []

		for dd in dev_data.split('|')[1:-1]:
			dev_stat = []
			dev_stat.append(elapsed_time_flag.search(dd).group(1))
			dev_stat.append(total_Mh_flag.search(dd).group(1))
			dev_stat.append(temperature_d_flag.search(dd).group(1))
			dev.append(dev_stat)
			
		j = 0
		for sd in stat_data.split('|')[1:-1]:
			if stat_pool_flag.search(sd) != None:
				#ignore pool stat in ' -o stats'
				break
			
			dev[j].append(len(module_id_flag.findall(sd)))
			
			temp = []
			for t in temperature_s_flag.findall(sd):
				temp.append(t.split('=')[1])
			dev[j].append(temp)
			
			fan = []
			for f in fan_flag.findall(sd):
				fan.append(f.split('=')[1])
			dev[j].append(fan)
			
			j += 1
		
		for pd in pool_data.split('|')[1:-1]:
			pool_stat = []
			pool_stat.append(pool_url_flag.search(pd).group(1))
			pool_stat.append(pool_alive_flag.search(pd).group(1))
			pool.append(pool_stat)
		
		miner.append(h)
		miner.append('Alive')
		try:
			miner.append(re.search(r'Elapsed=([^,]*),',summary).group(1))
		except AttributeError:
			miner.append('0')
		try:
			miner.append(total_Mh_flag.search(summary).group(1))
		except AttributeError:
			miner.append('0')
		miner.append(dev)
		miner.append(pool)
		data.append(miner)
		i += 1
		
	return data

if __name__ == '__main__':
	cfg = readconfig("./statreport.conf")
	if cfg['Log']['directory'][-1] == '/':
		cfg['Log']['directory'] += '/' 
	cfg['Miner']['miner_list'] = list(filter(None, (x.strip() for x in cfg['Miner']['miner_list'].splitlines())))	
	data = chkstat(cfg)
	for miner in data:
		print miner[0] + ': ' + miner[1] + ' ' + miner[2] + ' ' + miner[3]
		i = 1
		for dev_stat in miner[4]:
			print '\tModule #' + str(i) + ':'
			print '\t\tDevice Elapsed: ' + dev_stat[0]
			print '\t\tTotal MH: ' + dev_stat[1]
			print '\t\tTemperature: ' + dev_stat[2]
			print '\t\tModules Number: ' + str(dev_stat[3])
			print '\t\tTemperature List: ' + ','.join(dev_stat[4])
			print '\t\tFan Speed List: ' + ','.join(dev_stat[5])
			i += 1
		
		i = 1
		for pool_stat in miner[5]:
			print '\tPool #' + str(i) + ':'
			print '\t\tURL: ' + pool_stat[0]
			print '\t\tStatus: ' + pool_stat[1]
			i += 1
		print "------------------------------------------------------------------------------"
		
