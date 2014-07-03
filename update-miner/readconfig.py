#!/usr/bin/env python
import os
import ConfigParser
def readconfig(cfgfile):
	config = ConfigParser.ConfigParser()
	config.read(cfgfile)
	cfg = dict(config._sections)
	for k in cfg:
		cfg[k] = dict(config._defaults, **cfg[k])
		cfg[k].pop('__name__', None)

	cfg['Telnet']['miner_list'] = list(filter(None, (x.strip() for x in cfg['Telnet']['miner_list'].splitlines())))
	cfg['Telnet']['commands'] = list(filter(None, (x.strip() for x in cfg['Telnet']['commands'].splitlines())))
	return cfg

