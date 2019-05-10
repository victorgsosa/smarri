import cv2

from .abstract_drawer import AbstractDrawer
from collections import OrderedDict 

MOUTH_LANDMARKS_IDXS = OrderedDict([
	("top_lip", [0, 1, 2, 3, 4, 5, 6, 16, 15, 14, 13, 12]),
	("bottom_lip", [6, 7, 8 , 9, 10, 11, 12, 19, 18, 17, 16]),
])


class MouthDrawer(AbstractDrawer):
	def draw(self, image, shapes, color = (0, 0, 0), alpha = 0.25):
		mouths = shapes['mouth']
		overlay = image.copy()
		for mouth in mouths:
			for name, idx in MOUTH_LANDMARKS_IDXS.items():
				pts = mouth[idx]
				pts = pts.reshape((-1,1,2))
				cv2.fillPoly(overlay, [pts], color)
		cv2.addWeighted(overlay, alpha, image, 1 - alpha, 0, image)
