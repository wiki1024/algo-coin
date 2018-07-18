import threading
import queue
from decimal import *
import bisect
import datetime
from autobahn.twisted.websocket import WebSocketClientProtocol, \
    WebSocketClientFactory, connectWS


q = queue.Queue()


spot_btc_usdt_ticker = None
spot_btc_usdt_depth = None

this_week_btc_usdt_depth = None
this_week_btc_usdt_depth = None

next_week_usdt_depth = None
next_week_usdt_depth = None

quarter_btc_usdt_depth = None
quarter_btc_usdt_depth = None

def worker():
    while True:
        payload = q.get()
        if 'channel' in payload:
            channel = payload['channel']
            if channel == 'addChannel':
                print('addChannel')
            if channel == 'ok_sub_spot_btc_usdt_depth':
                process_spot_btc_usdt_depth(payload['data'])

# { asks, asks_keys, bids, bids_keys, timestamp }
def process_spot_btc_usdt_depth(data):
    raw_asks = data['asks']
    raw_bids = data['bids']
    recv_asks = [ [Decimal(pair[0[),Decimal(pair[1[)] for pair in raw_asks]
    recv_bids = [ [Decimal(pair[0[),Decimal(pair[1[)] for pair in raw_bids]
    if spot_btc_usdt_depth is None:
        #未初始化
        spot_btc_usdt_depth = {}
        recv_asks_keys = [pair[0] for pair in recv_asks] 
        recv_bids_keys = [pair[0] for pair in recv_bids]  
        spot_btc_usdt_depth['asks']= recv_asks
        spot_btc_usdt_depth['asks_keys']= recv_asks_keys
        spot_btc_usdt_depth['bids']= recv_bids
        spot_btc_usdt_depth['bids_keys']= recv_bids_keys
    else:
        #增量
        #asks
       iter_add_or_update_or_delete_spot_depth(recv_asks,'asks')
       iter_add_or_update_or_delete_spot_depth(recv_bids,'bids')
    spot_btc_usdt_depth['okex_timestamp']=datetime.fromtimestamp(data['timestamp']/ 1000.0)
    spot_btc_usdt_depth['recv_timestamp']=datetime.now()



def iter_add_or_update_or_delete_spot_depth(recv_list,a_b_type):
    source_keys = spot_btc_usdt_depth[a_b_type + '_keys']
    source_list = spot_btc_usdt_depth[a_b_type]
    for recv in recv_list:
        key = recv[0]
        volumn = recv[1]
        position = bisect.bisect_left(source_keys, key)
        if len(source_keys) != 0 and len(source_keys) != position:
            if source_keys[position] == key:
                #存在， 更新或删除
                if volumn==0:
                    source_list.pop(position)
                    source_keys.pop(position)
                else:
                    source_list[position][1]= volumn
            else:
                #新增
                source_list.insert(position, [key, volumn])
                source_keys.insert(position, key)
            






# {
#     spot:{
#         ticker:{
#               recv_timestamp,
#               timestamp,
#         },
#         depth:{

#         }
#     },
#     this_week:{
#         ticker:{

#         },
#         depth:{

#         }
#     },
#     next_week:{
#         ticker:{

#         },depth:{

#         }
#     },
#     quarter:{
#         ticker, depth
#     }
# }


class MyClientProtocol(WebSocketClientProtocol):
    def onConnect(self, response):
        print("Server connected: {0}".format(response.peer))

    def onOpen(self):
        print("WebSocket connection open.")

        def hello():
            # self.sendMessage(u"{'event':'addChannel','channel':'ok_sub_spot_btc_usdt_ticker'}".encode('utf8'))
            self.sendMessage(
                b"{'event':'addChannel','channel':'ok_sub_spot_btc_usdt_depth'}"
            )
            # self.sendMessage(b"{'event':'addChannel','channel':'ok_sub_futureusd_btc_ticker_quarter'}")
            # self.sendMessage(b'{"event":"ping"}')

        # start sending messages every second ..
        hello()

    def onMessage(self, payload, isBinary):
        import json
        # if isBinary:
        #     print("Binary message received: {0} bytes".format(len(payload)))
        # else:
        #   print("Text message received: {0}".format(payload.decode('utf8')))
        payload_array = json.loads(payload.decode('utf8'))
        if type(payload_array) is list:
            for payload in payload_array:
                q.put_nowait(payload)



    def onClose(self, wasClean, code, reason):
        print("WebSocket connection closed: {0}".format(reason))


if __name__ == '__main__':

    import sys

    from twisted.python import log
    from twisted.internet import reactor, ssl

    log.startLogging(sys.stdout)
    t = threading.Thread(target=worker)
    t.start()
    factory = WebSocketClientFactory("wss://real.okex.com:10441/websocket")
    factory.protocol = MyClientProtocol
    contextFactory = ssl.ClientContextFactory()
    connectWS(factory, contextFactory)
    reactor.run()