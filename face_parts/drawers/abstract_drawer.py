import cv2

from abc import ABC, abstractmethod

class AbstractDrawer(ABC):

	@abstractmethod
	def draw(self, image, shapes, color = (0, 0, 0), alpha = 0.25):
		pass

