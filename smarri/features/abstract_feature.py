from abc import ABC, abstractmethod

class AbstractFeature(ABC):
	@abstractmethod
	def get(self, image, shapes):
		pass