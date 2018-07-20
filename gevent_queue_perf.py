import gevent
from gevent.queue import Queue
from gevent.event import Event, AsyncResult
from datetime import datetime

import gc

tasks = Queue()
evt = Event()
numOfIter = 1000*1000

a = AsyncResult()


def worker(expected):
	while expected != 0:
		task = tasks.get()
		expected = expected - 1
	evt.set()


def boss(round):
	evt.clear()
	ss = datetime.now()
	for j in range(numOfIter):
		tasks.put(j)
	evt.wait()
	print(str(round) + "  " + str(numOfIter * 1.0 / (datetime.now() - ss).total_seconds()))


def setter():
	"""
	After 3 seconds set the result of a.
	"""
	gevent.sleep(3)
	a.set('Hello!')


def waiter():
	"""
	After 3 seconds the get call will unblock after the setter
	puts a value into the AsyncResult.
	"""
	print(a.get())


if __name__ == '__main__':
	for i in range(7):
		gc.collect()
		gevent.joinall([
			gevent.spawn(worker, numOfIter),
			gevent.spawn(boss, i),
		])
