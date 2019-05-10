import cv2

from .abstract_feature import AbstractFeature

class QRCodeFeature(AbstractFeature):
	def __init__(self):
		self._decoder = cv2.QRCodeDetector()

	def get(self, image, shapes):
		gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
		data,_,_ = self._decoder.detectAndDecode(gray)
		if len(data)>0:
			print("Decoded Data : {}".format(data))
		return data