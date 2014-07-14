#!/usr/bin/env python
from __future__ import print_function
import datetime
import sys
from poolrate import poolrate

def chkrate(data,data0,cfg,time,time0):

	if data !=None:
		print('Calculating hashrate ... ',end="")
		sys.stdout.flush()

	deltaT = datetime.timedelta(hours=26)

	t = []
	v1 = []
	v2 = []
	vp = []
	vps = []

	try:
		logfile = open(cfg['General']['hashrate_log'], 'r')
		time_flag = False
		for line in logfile:
			tmp = line.split(';')
			if time_flag:
				t.append((datetime.datetime.strptime(tmp[0],"%Y_%m_%d_%H_%M")-time).total_seconds())
				v1.append(float(tmp[1]))
				v2.append(float(tmp[2]))
				vp.append(float(tmp[3]))
				vps.append(float(tmp[4]))
				continue
			if datetime.datetime.strptime(tmp[0],"%Y_%m_%d_%H_%M") + deltaT > time:
				time_flag = True
		logfile.close()
	except IOError:
		logfile = open(cfg['General']['hashrate_log'], 'w')
		logfile.close()
		pass

	if data0 != None:
		t.append(0)

		dt = (time - time0).total_seconds()

		v1u  = [[0 for i2 in range(0,len(cfg['port_list'][i1]))]for i1 in range(0,len(cfg['miner_list']))]
		v2u  = [[0 for i2 in range(0,len(cfg['port_list'][i1]))]for i1 in range(0,len(cfg['miner_list']))]
		h  = [[0 for i2 in range(0,len(cfg['port_list'][i1]))]for i1 in range(0,len(cfg['miner_list']))]
		h0  = [[0 for i2 in range(0,len(cfg['port_list'][i1]))]for i1 in range(0,len(cfg['miner_list']))]
		tt  = [[0 for i2 in range(0,len(cfg['port_list'][i1]))]for i1 in range(0,len(cfg['miner_list']))]
		tt0  = [[0 for i2 in range(0,len(cfg['port_list'][i1]))]for i1 in range(0,len(cfg['miner_list']))]

		i = 0
		v1n = 0
		v2n = 0
		for mminer in data:
			j = 0
			try:mminer0 = data0[i]
			except:pass
			for miner in mminer[1:]:
				try:miner0 = mminer0[j+1]
				except:pass
				if miner[1] != "Dead":
					h[i][j] = float(miner[3])
					try:h0[i][j] = float(miner0[3])
					except:pass
					tt[i][j] = float(miner[2])
					try:tt0[i][j] = float(miner0[2])
					except:pass
					if tt[i][j] - tt0[i][j] > dt - int(cfg['HSplot']['delay_time']):
						v1u[i][j] = (h[i][j]-h0[i][j])/(tt[i][j]-tt0[i][j])
						v2u[i][j] = (h[i][j]-h0[i][j])/(tt[i][j]-tt0[i][j])
					elif miner[2] != '0':
						v1u[i][j] = h[i][j]/tt[i][j]
						v2u[i][j] = h[i][j]/dt
					else:
						pass
				v1n += v1u[i][j]
				v2n += v2u[i][j]
				j += 1
			i += 1

		v1.append(v1n)
		v2.append(v2n)
		print('Done.')

		print('Fetching pool hashrate data ... ',end="")
		sys.stdout.flush()
		sum_pool_rate, pool_rate = poolrate(cfg)
		print('Done.')

		vp.append(float(pool_rate))
		vps.append(float(sum_pool_rate))

		logfile = open(cfg['General']['hashrate_log'], 'a')
		logfile.write(time.strftime('%Y_%m_%d_%H_%M')+';'+str(v1n)+';'+str(v2n)+';'+str(pool_rate)+';'+str(sum_pool_rate)+'\n')
		logfile.close()

	return [t,v1,v2,vp,vps]

