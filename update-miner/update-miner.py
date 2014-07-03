#!/usr/bin/env python
from __future__ import print_function
import telnetlib
import sys
import time
import threading
import Queue
from readconfig import readconfig

def telnetthread(miner_queue,lock,commands,retry):
	while True:
		try:
			(miner_ip, miner_id) = miner_queue.get(False)
			time_out = 9
			while True:
				time_out += 1
				tn = telnetlib.Telnet()

				err_conn_flag = False
				for k in range(0,retry):
					## try connecting for some times
					try:
						tn.open( miner_ip,23, time_out )
						break
					except:
						tn.close()
						lock.acquire()
						if k < retry -1:
							print('\033[1m\033[33mCannot connect to ' + miner_ip + '. Try Again.\033[0m')
						else:
							print('\033[31mCannot connect to ' + miner_ip + '. Skip.\033[0m')
						lock.release()
						err_conn_flag = True
				if err_conn_flag:
					break

				try:
					tn.read_until('root@OpenWrt:/# ')
					for c in commands:
						tn.write(c + '\n')
						tn.read_until('root@OpenWrt:/# ')
					tn.write('exit\n')
					tn.read_all()
				except:
					tn.close()
					lock.acquire()
					print("\033[31mConnection to " + miner_ip + " lost. Extend time-out and try again.\033[0m")
					lock.release()
					continue

				tn.close()

				lock.acquire()
				print("Update complete @" + miner_ip + ".")
				lock.release()
				break
		except Queue.Empty:
			break


if __name__ == '__main__':

	if len(sys.argv) < 1:
		cfg = readconfig('./update.conf')
	else:
		cfg = readconfig(sys.argv[1])
	miner_queue = Queue.Queue()
	lock = threading.Lock()
	for i in range(0,len(cfg['Telnet']['miner_list'])):
		miner_queue.put((cfg['Telnet']['miner_list'][i],i))

	threads = []
	for i in range(0,int(cfg['Telnet']['threads_num'])):
		threads.append(threading.Thread( target=telnetthread, args=( miner_queue, lock,cfg['Telnet']['commands'], int(cfg['Telnet']['retry']), ) ))
	for t in threads:
		t.start()
	for t in threads:
		t.join()
