from .abstract_recommender import AbstractRecommender
from utils.decorators import timing

class DictRecommender(AbstractRecommender):
	def __init__(self, feature, colors={} ):
		self._feature = feature
		self._colors = colors

	@timing
	def predict(self, image, shapes):
		colors = [self._colors[value] for value in self._feature.get(image, shapes) if value in self._colors]
		return colors
