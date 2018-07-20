import queue

stream = queue.Queue()

from stream.rest import run as rest

from stream.consumer import run as consumer
