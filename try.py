import requests
import stream

if __name__ == '__main__':
	# r = requests.get("https://www.okex.com/api/v1/future_depth.do?symbol=btc_usdt&contract_type=this_week&size=200")
	# print(r.json())
	stream.consumer()
	stream.rest()
