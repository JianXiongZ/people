#!/usr/bin/env python
import telnetlib
import re
import time

def chkstat(hosts):

    dev_flag = re.compile('MHS[^,=]*=0[.]00,')
    pool_flag = re.compile('Status=Alive')

    err_hosts=[]
    err_devs=[]
    err_pools=[]

    stats={}
    #dev_stats=[]
    #pool_stats=[]
    
    i = 1
    for h in hosts:
	
	tn = telnetlib.Telnet()

	conn_flag = False
	for k in range(0,5):
	    try:
		print 'Conneting ' + h +' ...',
		tn.open(h,23)
		print 'Done.'
		break
	    except:
		tn.close()
		print 'Error' + ('. Try Again.' if k < 4 else '. Skip.')
		conn_flag = True
	if conn_flag:
	    err_hosts.append(h)
	    continue
		
	## read devs stats ##
	tn.write('cgminer-api -o devs\n')

	## read pools stats ##
	tn.write('cgminer-api -o pools\n')

	tn.write('exit\n')

	tmp = tn.read_all().split('cgminer-api')

	dev_stats = tmp[-2]
	pool_stats = tmp[-1]	

	#print dev_stats
	#print pool_stats

	tn.close()

	stats[h] = len(dev_stats.split('|')[1:-1])
	
	j=1
	for ds in dev_stats.split('|')[1:-1]:
	    if dev_flag.search(ds):
		err_devs.append([i,j])
	    j = j + 1

	j=1
	for ps in pool_stats.split('|')[1:-1]:
	    if not pool_flag.search(ps):
		err_pools.append([i,j])
	    j = j + 1

	i = i + 1
	
	
    return (stats,err_hosts,err_devs,err_pools)

if __name__ == '__main__':

    hosts=[]
    f = open('minerlist.txt','r')
    lines = f.read().split('\n')
    for line in lines:
        if line == '':
            continue
        hosts.append(line)

    (err_devs,err_pools)=chkstat(hosts)
    #print err_devs
    #print err_pools

