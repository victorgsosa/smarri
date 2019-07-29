from collections import OrderedDict

import numpy as np
import argparse
import imutils
import dlib
import cv2


def shape_to_np(shape, dtype="int"):
	# initialize the list of (x, y)-coordinates
	coords = np.zeros((shape.num_parts, 2), dtype=dtype)

	# loop over all facial landmarks and convert them
	# to a 2-tuple of (x, y)-coordinates
	for i in range(0, shape.num_parts):
		coords[i] = (shape.part(i).x, shape.part(i).y)

	# return the list of (x, y)-coordinates
	return coords


# define a dictionary that maps the indexes of the facial
# landmarks to specific face regions
FACIAL_LANDMARKS_IDXS = OrderedDict([
	("mouth", (48, 68)),
	("right_eyebrow", (17, 22)),
	("left_eyebrow", (22, 27)),
	("right_eye", (36, 42)),
	("left_eye", (42, 48)),
	("nose", (27, 35)),
	("jaw", (0, 17))
])
 
# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-p", "--shape-predictor", dest="shape_predictor", required=True,
	help="path to facial landmark predictor")
ap.add_argument("-f", "--face-part", dest='face_part', required=True,
	help="face_part")
ap.add_argument('-s', '--source', dest='source',type=int, default=0, help='device index')
args = ap.parse_args()
alpha = 0.2
 
# initialize dlib's face detector (HOG-based) and then create
# the facial landmark predictor
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(args.shape_predictor)
name = args.face_part
cap = cv2.VideoCapture(args.source)
 
while(True):
	# load the input image, resize it, and convert it to grayscale

	_, image = cap.read()
	size = image.shape
	scaled = imutils.resize(image, width=500)
	scaled_size = scaled.shape
	h = scaled_size[0] / size[0]
	w = scaled_size[1] / size[1]
	gray = cv2.cvtColor(scaled, cv2.COLOR_BGR2GRAY)
	
	# detect faces in the grayscale image
	rects = detector(gray, 1)
	clone = image.copy()
	overlay = image.copy()
	# loop over the face detections
	for (i, rect) in enumerate(rects):
		# determine the facial landmarks for the face region, then
		# convert the landmark (x, y)-coordinates to a NumPy array
		shape = predictor(gray, rect)
		shape = shape_to_np(shape)
		shape[:, 0] = shape[:, 0] / h
		shape[:, 1] = shape[:, 1] / w
		(i,j) = FACIAL_LANDMARKS_IDXS[name]

	 
		# loop over the subset of facial landmarks, drawing the
		# specific face part
		hull = cv2.convexHull(shape[i:j])
		cv2.drawContours(overlay, [hull], -1, (249,135,135), -1)
		overlay = cv2.resize(overlay, (size[1], size[0]), interpolation = cv2.INTER_AREA)
		cv2.addWeighted(overlay, alpha, clone, 1 - alpha, 0, clone)
	cv2.cvtColor(clone, cv2.COLOR_BGRA2BGR)

	cv2.putText(clone, name, (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
				0.7, (0, 0, 255), 2)
	cv2.imshow("Image", clone)
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break