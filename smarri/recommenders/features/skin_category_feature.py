import numpy as np

from .skin_color_feature import SkinColorFeature
from collections import OrderedDict

CATEGORIES = np.array([[118.1975, 143.7675, 204.41],[103.185, 129.35, 186.31], [96.53, 121.575, 168.6075]])

class SkinCategoryFeature(SkinColorFeature):
	def get(self, image, shapes):
		colors = super().get(image, shapes)
		categories = [ self._category(color) for color in colors]
		return categories

	def _category(self, color):
		dist = CATEGORIES - color
		dist = np.sum(dist * dist, axis=1)
		category = np.argmin(dist, axis=0)
		return category