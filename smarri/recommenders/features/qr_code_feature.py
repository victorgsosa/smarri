import cv2
import pyzbar.pyzbar as pyzbar
import logging

from .abstract_feature import AbstractFeature


class QRCodeFeature(AbstractFeature):

	def get(self, image, shapes):
		gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
		objects = pyzbar.decode(gray)
		if objects: 
			log = logging.getLogger()
			log.info("Detected QR value %s" % objects)
		return [object.data.decode('ascii') for object in objects]