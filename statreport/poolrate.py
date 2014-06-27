#!/usr/bin/env python

import json
import urllib
import urllib2
import hashlib
import hmac
import time

def poolrate(cfg):
	url1 = 'https://cex.io/api/ghash.io/hashrate'
	url2 = 'https://cex.io/api/ghash.io/workers'

	proxy_handler = urllib2.ProxyHandler({})
	opener = urllib2.build_opener(proxy_handler)
	urllib2.install_opener(opener)

	try:
		key = cfg['Pool']['api_key']
		nonce = '{:.0f}'.format(time.time()*1000)
		signature = hmac.new(cfg['Pool']['api_secret_key'], msg = nonce + cfg['Pool']['username'] + key, digestmod=hashlib.sha256).hexdigest().upper()
		post_content = { 'key': key, 'signature': signature, 'nonce': nonce}

		param = urllib.urlencode(post_content)

		request1 = urllib2.Request(url1, param, {'User-agent': 'bot-cex.io-' + cfg['Pool']['username']})
		js1 = urllib2.urlopen(request1).read()
		dict1 = json.loads(js1)
		request2 = urllib2.Request(url2, param, {'User-agent': 'bot-cex.io-' + cfg['Pool']['username']})
		result2 = urllib2.urlopen(request2).read()
		dict2 = json.loads(js2)

		return (dict1['last1h'],dict2[cfg['Pool']['workername']]['last1h'])
	except:
		return ('0','0')
