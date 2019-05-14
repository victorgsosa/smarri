from abc import ABC, abstractmethod

class AbstractRecommender(ABC):

	@abstractmethod
	def predict(self):
		pass