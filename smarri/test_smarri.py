import gi
import logging
import argparse
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib
from views.test_main import MainWindow
from utils.stream import VideoStream
from detector import FacePartsDetector

if __name__ == '__main__':
	ap = argparse.ArgumentParser()
	ap.add_argument('-p', '--shape-predictor', dest='shape_predictor', required=True,help='path to facial landmark predictor')
	ap.add_argument('-s', '--source', dest='source',type=int, default=0, help='device index')
	ap.add_argument('-a', '--alpha', dest='alpha', type=float, default=0.25, help='alpha')
	args = ap.parse_args()
	detector = FacePartsDetector(args.shape_predictor, ['mouth', 'right_eye', 'left_eye', 'right_eyebrow', 'left_eyebrow', 'nose', 'jaw'])
	stream = VideoStream(args.source, detector).start()
	smarry = MainWindow(stream)
	smarry.connect("destroy", Gtk.main_quit)
	smarry.show_all()
	GLib.idle_add(smarry.show_frame)
	logging.basicConfig(level=logging.WARN,  format='%(asctime)s [%(process)d] - %(name)s - %(levelname)s - %(message)s')
	Gtk.main()