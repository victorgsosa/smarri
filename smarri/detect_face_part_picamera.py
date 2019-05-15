import argparse
import imutils
import cv2
import drawers as drw
import recommenders
import recommenders.features as features


from collections import OrderedDict 
from detector import FacePartsDetector
from picamera.array import PiRGBArray
from picamera import PiCamera



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

SKIN_COLORS = {
	0: { 'mouth': [[0, 255, 0], [12,67,34], [255, 230, 156]], 'eyes': [[0, 255, 0], [12,67,34], [255, 230, 156]] },
	1: { 'mouth': [[0, 0, 255], [12,255,34], [255, 230, 156]], 'eyes': [[0, 0, 255], [12,255,34], [255, 230, 156]] },
	2: { 'mouth': [[255,0 , 0], [12,67,34], [255, 100, 156]], 'eyes': [[255,0 , 0], [12,67,34], [255, 100, 156]] },
}

QR_CODE_COLORS = {
	'0000001': {'mouth': [[0, 255, 213]]},
	'0000002': {'mouth': [[123, 123, 213]]},
	'0000003': {'mouth': [[200, 255, 213]]},
	'0000004': {'mouth': [[110, 255, 213]]},
	'0000005': {'mouth': [[150, 255, 213]]},
	'0000006': {'eyes': [[0, 255, 213]]},
	'0000007': {'eyes': [[123, 123, 213]]},
	'0000008': {'eyes': [[200, 255, 213]]},
	'0000009': {'eyes': [[110, 255, 213]]},
	'0000010': {'eyes': [[150, 255, 213]]},
}


 
# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument('-p', '--shape-predictor', dest='shape_predictor', required=True,
	help='path to facial landmark predictor')
ap.add_argument('-s', '--source', dest='source',type=int, default=0, help='device index')
ap.add_argument('-a', '--alpha', dest='alpha', type=float, default=0.25, help='alpha')
args = ap.parse_args()
 
detector = FacePartsDetector(args.shape_predictor, ['mouth', 'right_eye', 'left_eye', 'right_eyebrow', 'left_eyebrow', 'nose', 'jaw'])
camera = PiCamera()
rawCapture = PiRGBArray(camera)

mouth_drawer = DRAWERS['mouth']
eyes_drawer = DRAWERS['eyes']
skin_color = features.SkinCategoryFeature()
qr_code = features.QRCodeFeature()
skin_rec = recommenders.DictRecommender(skin_color, SKIN_COLORS)
qr_rec = recommenders.DictRecommender(qr_code, QR_CODE_COLORS)

while(True):
	# load the input image, resize it, and convert it to grayscale

	camera.capture(rawCapture, format='bgr')
	image = rawCapture.array
	if image is not None:
		image = imutils.resize(image, width=900)
		gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
		shapes = detector.detect(gray)
		skin_predict = skin_rec.predict(image, shapes)
		qr_predict = qr_rec.predict(image, shapes)	
		print(qr_predict)
		eyes_drawer.draw(image, shapes, ( 183, 163, 255), 0.1)
		mouth_drawer.draw(image, shapes, ( 99, 49,  222), 0.2)

		cv2.imshow('Image', image)
		if cv2.waitKey(1) & 0xFF == ord('q'):
			cv2.destroyAllWindows()
			break