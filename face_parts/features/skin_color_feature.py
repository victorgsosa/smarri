import numpy as np
import cv2

from .abstract_feature import AbstractFeature 

RADIUS = 10	

class SkinColorFeature(AbstractFeature):
	def _clamp(self, n, min_val, max_val):
		return max(min_val , min(n , max_val))

	def get(self, image, shapes):
		colors = []
		for nose in shapes['nose']:
			detect_point = nose[2]
			x = self._clamp(detect_point[0], RADIUS, image.shape[1]-1-RADIUS)
			y = self._clamp(detect_point[1], RADIUS, image.shape[0]-1-RADIUS)
			xmin = x - RADIUS
			xmax = x + RADIUS
			ymin = y - RADIUS
			ymax = y + RADIUS
			color = image[ymin:ymax, xmin:xmax]
			color = np.mean(color, axis=(0,1))
			colors.append(color)
			#cv2.circle(image, tuple(detect_point), RADIUS, tuple(color) , -1)
		return colors
			


