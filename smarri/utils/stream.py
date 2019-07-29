import recommenders
import recommenders.features as features
import cv2


from threading import Thread
from detector import FacePartsDetector
from recommenders import DictRecommender


class VideoStream(object):

	def __init__(self, path , detector: FacePartsDetector):
		self.stream = self.stream = cv2.VideoCapture(path)
		self.stopped = False
		self.detector = detector
		_, self.image = self.stream.read()
		self.shapes = self.detector.detect(self.image)

	def start(self):
		t = Thread(target=self.update, args=())
		t.daemon = True
		t.start()
		return self

	def update(self):
		while(True):
			if self.stopped:
				return
			_, image = self.stream.read()
			if image is not None:
				
				shapes = self.detector.detect(image)

				self.image = image
				self.shapes = shapes
			

	def read(self):
		return self.image, self.shapes


	def stop(self):
		self.stopped = True

class RecommenderStream(object):
	def __init__(self, stream: VideoStream, recommender: DictRecommender):
		self.stream = stream
		self.recommender = recommender
		image, shapes = stream.read()
		self.prediction = recommender.predict(image, shapes)
		self.stopped = False

	def start(self):
		t = Thread(target=self.update, args=())
		t.daemon = True
		t.start()
		return self

	def update(self):
		while(True):
			if self.stopped:
				return
			image, shapes = self.stream.read()
			self.prediction = self.recommender.predict(image, shapes)

	def read(self):
		return self.prediction

	def stop(self):
		self.stopped = True
