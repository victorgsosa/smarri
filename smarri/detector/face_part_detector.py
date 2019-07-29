import numpy as np
import dlib
import imutils
import cv2

from collections import OrderedDict 
from utils.decorators import timing

FACIAL_LANDMARKS_IDXS = OrderedDict([
	("mouth", (48, 68)),
	("right_eyebrow", (17, 22)),
	("left_eyebrow", (22, 27)),
	("right_eye", (36, 42)),
	("left_eye", (42, 48)),
	("nose", (27, 35)),
	("jaw", (0, 17))
])


class FacePartsDetector(object):

	def __init__(self, predictor_path, part_names = []):
		self._part_names = part_names
		self._detector = dlib.get_frontal_face_detector()
		self._predictor = dlib.shape_predictor(predictor_path)

	def _shape_to_np(self, shape, dtype="int"):
		coords = np.zeros((shape.num_parts, 2), dtype=dtype)
		for i in range(0, shape.num_parts):
			coords[i] = (shape.part(i).x, shape.part(i).y)
		return coords

	@timing
	def detect(self, image):
		true_shape = image.shape
		if image.shape[1] > 500:
			scaled = imutils.resize(image, width = 500)
		else:
			scaled = image
		scaled_shape = scaled.shape
		hr = scaled_shape[0] / true_shape[0]
		wr = scaled_shape[1] / true_shape[1]
		gray = cv2.cvtColor(scaled, cv2.COLOR_BGR2GRAY)
		rects = self._detector(gray, 1)
		parts = { part_name: [] for part_name in self._part_names }
		for ( _, rect) in enumerate(rects):
			shape = self._predictor(gray, rect)
			shape = self._shape_to_np(shape)
			shape[:, 0] = shape[:, 0] / hr
			shape[:, 1] = shape[:, 1] / wr
			for part_name in self._part_names:
				(i,j) = FACIAL_LANDMARKS_IDXS[part_name]
				parts[part_name].append(shape[i:j])
		return parts

