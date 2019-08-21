import logging
import numpy as np


from .skin_color_feature import SkinColorFeature
from collections import OrderedDict


CATEGORIES = np.array([[9.535,  130.3075, 118.01],[ 8.955, 115.4875, 172.2525], [10.075, 126.75, 74.195]])

class SkinCategoryFeature(SkinColorFeature):
	def get(self, image, shapes):
		colors = super().get(image, shapes)
		categories = [ self._category(color) for color in colors]
		return categories

	def _category(self, color):
		dist = CATEGORIES - color
		dist = np.sum(dist * dist, axis=1)
		category = np.argmin(dist, axis=0)
		logging.debug("Skin category %d" % category)
		return category