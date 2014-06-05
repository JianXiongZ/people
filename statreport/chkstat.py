#!/usr/bin/env python
import telnetlib
import re
import time

def read_eff(telnethost):
    delay = 0.1
    s0=''
    while True:
        time.sleep(delay)
        s = telnethost.read_very_eager()
        if s == '' and s0 != '':
            break
        if s != '':
	    s0 += s
    return s0

def chkstat(hosts):

    dev_flag = re.compile('MHS[^,=]*=0[.]00,')
    pool_flag = re.compile('Status=Alive')

    err_devs=[]
    err_pools=[]

    #dev_stats=[]
    #pool_stats=[]
    
    i = 1
    for h in hosts:
	tn = telnetlib.Telnet(h,23)
	
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
	
	
    return (err_devs,err_pools)

if __name__ == '__main__':

    hosts=[]
    f = open('minerlist.txt','r')
    lines = f.read().split('\n')
    for line in lines:
        if line == '':
            continue
        hosts.append(line)

    (err_devs,err_pools)=chkstat(hosts)
    print err_devs
    print err_pools

