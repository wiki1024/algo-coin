import threading
import queue
import gc
from datetime import datetime

q = queue.Queue(1000)

evt = threading.Event()


def msg_handler(expected):
	while expected != 0:
		msg = q.get()
		expected = expected - 1
	evt.set()


if __name__ == '__main__':
	numOfIter = 1000*1000
	for i in range(7):
		gc.collect()
		evt.clear()
		t = threading.Thread(target=msg_handler, args=(numOfIter,))
		t.start()
		ss = datetime.now()
		for j in range(numOfIter):
			q.put(j)
		evt.wait()
		print(numOfIter * 1.0 / (datetime.now() - ss).total_seconds())
