import numpy as np
import dlib

from collections import OrderedDict 

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

	def detect(self, image):
		rects = self._detector(image, 1)
		parts = { part_name: [] for part_name in self._part_names }
		for ( _, rect) in enumerate(rects):
			shape = self._predictor(image, rect)
			shape = self._shape_to_np(shape)
			for part_name in self._part_names:
				(i,j) = FACIAL_LANDMARKS_IDXS[part_name]
				parts[part_name].append(shape[i:j])
		return parts

