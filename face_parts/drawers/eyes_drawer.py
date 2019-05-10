import cv2 
import numpy as np

from .abstract_drawer import AbstractDrawer
from collections import OrderedDict

EYE_LANDMARKS_IDS = OrderedDict([
	('eye',  [0, 1, 2, 3]),
	('eyebrow', [0, 1, 3, 4])
])

class EyesDrawer(AbstractDrawer):

	def draw(self, image, shapes, color = (0, 0, 0), alpha = 0.25):
		overlay = image.copy()
		for left_eye, right_eye, left_eyebrow, right_eyebrow in zip(shapes['left_eye'], shapes['right_eye'], shapes['left_eyebrow'], shapes['right_eyebrow']):
			left_eye_pts = left_eye[EYE_LANDMARKS_IDS['eye']]
			right_eye_pts = right_eye[EYE_LANDMARKS_IDS['eye']]
			left_eyebrow_pts = left_eyebrow[EYE_LANDMARKS_IDS['eyebrow']]
			right_eyebrow_pts = right_eyebrow[EYE_LANDMARKS_IDS['eyebrow']]
			left_pts = np.concatenate(( left_eye_pts, np.flip(((left_eye_pts + left_eyebrow_pts) / 2).astype(np.int64), 0)), axis = 0)
			right_pts = np.concatenate(( right_eye_pts, np.flip(((right_eye_pts + right_eyebrow_pts) / 2).astype(np.int64), 0)), axis = 0)
			left_pts = left_pts.reshape((-1,1,2))
			right_pts = right_pts.reshape((-1,1,2))
			cv2.fillPoly(overlay, [left_pts], color)
			cv2.fillPoly(overlay, [right_pts], color)
		cv2.addWeighted(overlay, alpha, image, 1 - alpha, 0, image)

