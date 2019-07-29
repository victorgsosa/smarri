import logging
import time


def timing(function):
	log = logging.getLogger(function.__module__)
	def wrap(*args):
		time1 = time.time()
		ret = function(*args)
		time2 = time.time()
		log.debug('%s function took %0.3f ms', function.__name__, (time2-time1)*1000.0)
		return ret
	return wrap