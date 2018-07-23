import threading

from strategy import this_week
from strategy import next_week
from strategy import quarter
from stream import stream

store = {
	'spot': {
		'ticker': None,
		'depth': None,
	},
	'this_week': {
		'ticker': None,
		'depth': None,
	},
	'next_week': {
		'ticker': None,
		'depth': None,
	},
	'quarter': {
		'ticker': None,
		'depth': None,
	}
}

callbacks = {
	'this_week': this_week.calculate_signals,
	'next_week': next_week.calculate_signals,
	'quarter': quarter.calculate_signals
}


def worker():
	while True:
		payload = stream.get()
		channel, sub_type = payload['channel']
		recv_timestamp = payload['recv_timestamp']
		send_timestamp = payload['send_timestamp']
		diff = recv_timestamp - send_timestamp
		print(channel + '_' + sub_type + ' delay ' + str(diff.total_seconds() * 1000) + 'ms')
		if channel in store:
			store[channel][sub_type] = payload
		else:
			print('unknown channel ' + channel)
		if channel in callbacks and callbacks[channel] is not None:
			if store['spot']['ticker'] is not None and store['spot']['depth'] is not None and store[channel]['ticker'] is not None and store[channel]['depth'] is not None:
				try:
					callbacks[channel](store['spot']['ticker']['data'], store['spot']['depth']['data'], store[channel]['ticker']['data'], store[channel]['depth']['data'])
				except Exception as ex:
					print('callback exception')
					print(ex)


def run():
	# import logging
	# logging.basicConfig(level=logging.DEBUG)
	t = threading.Thread(target=worker)
	t.start()
