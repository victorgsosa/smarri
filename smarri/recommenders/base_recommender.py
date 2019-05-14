from .abstract_recommender import AbstractRecommender


class DictRecommender(AbstractRecommender):
	def __init__(self, feature, colors={} ):
		self._feature = feature
		self._colors = colors

	def predict(self, image, shapes):
		colors = [self._colors[value] for value in self._feature.get(image, shapes)]
		return colors
