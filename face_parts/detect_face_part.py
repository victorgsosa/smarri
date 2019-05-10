import argparse
import imutils
import cv2
import drawers as drw
import features

from collections import OrderedDict 
from detector import FacePartsDetector



PART_NAMES = OrderedDict(
	[
		('mouth', ['mouth']),
		('eyes', ['right_eye', 'left_eye', 'right_eyebrow', 'left_eyebrow'])
	]
	)

DRAWERS = OrderedDict(
	[
		('mouth', drw.MouthDrawer()),
		('eyes', drw.EyesDrawer())	
	]
	)

 
# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument('-p', '--shape-predictor', dest='shape_predictor', required=True,
	help='path to facial landmark predictor')
ap.add_argument('-s', '--source', dest='source',type=int, default=0, help='device index')
ap.add_argument('-a', '--alpha', dest='alpha', type=float, default=0.25, help='alpha')
args = ap.parse_args()
 
detector = FacePartsDetector(args.shape_predictor, ['mouth', 'right_eye', 'left_eye', 'right_eyebrow', 'left_eyebrow', 'nose', 'jaw'])
cap = cv2.VideoCapture(args.source)

mouth_drawer = DRAWERS['mouth']
eyes_drawer = DRAWERS['eyes']
skin_color = features.SkinColorFeature()
qr_code = features.QRCodeFeature()
while(True):
	# load the input image, resize it, and convert it to grayscale

	_, image = cap.read()
	image = imutils.resize(image, width=500)
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	
	shapes = detector.detect(gray)
	skin_color.get(image, shapes)
	qr_code.get(image, shapes)	
	eyes_drawer.draw(image, shapes, ( 183, 163, 255), 0.1)
	mouth_drawer.draw(image, shapes, ( 99, 49,  222), 0.2)

	cv2.imshow('Image', image)
	if cv2.waitKey(1) & 0xFF == ord('q'):
		cv2.destroyAllWindows()
		break