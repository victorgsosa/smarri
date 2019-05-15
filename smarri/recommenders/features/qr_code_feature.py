import cv2
import pyzbar.pyzbar as pyzbar

from .abstract_feature import AbstractFeature


class QRCodeFeature(AbstractFeature):

	def get(self, image, shapes):
		gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
		objects = pyzbar.decode(gray)
		if len(objects)>0:
			print("Decoded Data : {}".format(objects))
		return [object.data.decode('ascii') for object in objects]