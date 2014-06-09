#!/usr/bin/env python
from statlogging import readlog

import matplotlib
matplotlib.use('Agg') 
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
import numpy as np

import datetime
import re
import os



def plot(time0,logdir):
	
	DELAY_TIME = 180
	
	
	deltaT = datetime.timedelta(1)
	xmllog = []
	
	t_datetime=[]
	#find log file in range from $time-$deltaT to $time
	for logfile in sorted(os.listdir(logdir),reverse=True):
		if re.match(r'log-(\d+_){4}\d+\.xml',logfile):
			logtime = datetime.datetime.strptime(logfile.strip('log-').strip('.xml'),"%Y_%m_%d_%H_%M")
			xmllog.append(logfile)
			if logtime + deltaT < time0:
				break
	if len(xmllog) < 2:
		print "More log files are needed for plotting."
		return 1


	#read hash num & elapsed time into $h[time point(0:)][miner No][]
	#calculate hash speed into v[time point(ignore #1)]
	
	xmllog = xmllog[::-1]
	
	h = []
	t = []
	v = []

	(data,time) = readlog(logdir,xmllog[0])
	ht=[]
	for i in range(0,len(data)):
		if data[i][1] == "Alive":
			ht.append( [ float(data[i][3]),float(data[i][2]) ] )
		else:
			ht.append( [0,0] )
	h.append(ht)
	t.append((time-time0).total_seconds())
	
	for k in range(1,len(xmllog)):
		(data,time) = readlog(logdir,xmllog[k])
		tt = (time-time0).total_seconds()
		ht=[]
		vt=[]
		for i in range(0,len(data)):
			if data[i][1] == "Dead":
				vt.append(0)
				ht.append( [0,0] )
			else:
				ht.append( [ float(data[i][3]),float(data[i][2]) ] )
				if ht[i][1] - h[k-1][i][1] > tt - t[k-1] - DELAY_TIME: 
					vt.append((ht[i][0]-h[k-1][i][0])/(ht[i][1]-h[k-1][i][1]))
				elif data[i][2] != '0':
					vt.append(ht[i][0]/ht[i][1])
				else:
					vt.append(0)
		t.append(tt)	
		h.append(ht)
		v.append(vt)
	
	t = t[1:]

	#total hash speed 
	vm = []
	for k in range(0,len(v)):
		vm.append( sum(v[k]) )
		t[k] = t[k]/3600.0
	
	
	x = np.array(t)
	y = np.array(vm)
	ymax = np.amax(y)
	
	f = interp1d(x, y, kind='cubic')
	xnew = np.linspace(t[0], t[-1], 40)
	
	plt.plot(xnew,f(xnew),'-')
	
	fig = plt.gcf()
	fig.set_size_inches(1024.0/fig.get_dpi(),768.0/fig.get_dpi())


	ax=plt.gca()  
	ax.set_xticks(np.linspace(-24,0,13))
	ax.set_xticklabels( ('-24', '-22', '-20', '-18', '-16',  '-14',  '-12',  '-10', '-8' , '-6' , '-4' , '-2' , '0' ))  
	
	ymax_s = str(int(ymax))
	ylim = int(ymax_s[0])*(10 ** (len(ymax_s)-1)) + (int(ymax_s[1])+1)*(10 ** (len(ymax_s)-2))
	print ylim
	ylabel = ['0']
	for i in range(1,int(ymax_s[0])*10 + 2 + int(ymax_s[1]) ):
		ylabel.append(str(i*(10 ** (len(ymax_s)-2))))
	print ylabel
	ax.set_yticks(np.linspace(0,ylim,int(ymax_s[0])*10 + 1 + int(ymax_s[1])))
	ax.set_yticklabels( tuple(ylabel))  



	plt.savefig("test.png")
		
	
	


if __name__ == '__main__':
	plot(datetime.datetime.now(),'./log/')