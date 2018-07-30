import gevent.monkey

gevent.monkey.patch_socket()

import gevent
import requests
from datetime import datetime
from decimal import *
from stream import stream


def task(channel, url, converter):
	import logging

	logging.basicConfig(level=logging.DEBUG)
	while True:
		try:
			send_timestamp = datetime.now()
			res = requests.get(url)
			json = res.json()
			sys_timestamp, data = converter(json)
			stream.put_nowait(
				{'channel': channel, 'data': data, 'sys_timestamp': sys_timestamp, 'recv_timestamp': datetime.now(), 'send_timestamp': send_timestamp})
		except Exception as ex:
			print(ex)
		gevent.sleep(1)


def spot_ticker_converter(source):
	sys_timestamp = datetime.fromtimestamp(int(source['date']) / 1000.0)
	ticker = source['ticker']
	for k, v in ticker.items():
		ticker[k] = Decimal(v)
	return sys_timestamp, ticker


def depth_converter(source):
	asks = [[Decimal(pair[0]), Decimal(pair[1])] for pair in source['asks']]
	bids = [[Decimal(pair[0]), Decimal(pair[1])] for pair in source['bids']]
	return None, {'asks': asks, 'bids': bids}


def run():
	gevent.joinall([
		gevent.spawn(task, ('spot', 'ticker'), 'https://www.okex.com/api/v1/ticker.do?symbol=btc_usdt', spot_ticker_converter),
		gevent.spawn(task, ('spot', 'depth'), 'https://www.okex.com/api/v1/depth.do?symbol=btc_usdt', depth_converter),
		gevent.spawn(task, ('this_week', 'ticker'), 'https://www.okex.com/api/v1/future_ticker.do?symbol=btc_usdt&contract_type=this_week', spot_ticker_converter),
		gevent.spawn(task, ('next_week', 'ticker'), 'https://www.okex.com/api/v1/future_ticker.do?symbol=btc_usdt&contract_type=next_week', spot_ticker_converter),
		gevent.spawn(task, ('this_week', 'depth'), 'https://www.okex.com/api/v1/future_depth.do?symbol=btc_usdt&contract_type=this_week&size=200', depth_converter),
		gevent.spawn(task, ('next_week', 'depth'), 'https://www.okex.com/api/v1/future_depth.do?symbol=btc_usdt&contract_type=next_week&size=200', depth_converter),
	])
