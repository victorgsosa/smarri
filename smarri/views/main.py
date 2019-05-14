import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GLib, GdkPixbuf
import cv2
import numpy as np
from views.ColorPalette import ColorPalette

import argparse
import imutils
import drawers as drw
import features

from detector import FacePartsDetector


eyePalette = {'color1': [77,0,0],
             'color2': [103,4,34],
             'color3': [133,4,56],
             'color4': [64,3,62],
             'color5': [5,0,58],
             'color6': [178,216,216],
             'color7': [102,178,178],
             'color8': [0,128,128],
             'color9': [0,102,102],
             'color10': [0,76,76],
             'color11': [141,85,36],
             'color12': [198,134,66],
             'color13': [224,172,105],
             'color14': [241,194,125],
             'color15': [255,219,172]}

lipstickPalette = {'color1': [249,135,135],
             'color2': [231,106,106],
             'color3': [214,91,91],
             'color4': [193,75,75],
             'color5': [184,63,63],
             'color6': [249,21,21],
             'color7': [208,9,9],
             'color8': [150,16,16],
             'color9': [171,0,0],
             'color10': [105,0,0]}



class MainWindow(Gtk.Window):

    def __init__(self):
        
        Gtk.Window.__init__(self, title="Smart Make Up Mirror")
        self.set_border_width(10)
        self.set_size_request(self.get_screen().get_width(), self.get_screen().get_height())

        self.mirror = Gtk.Image.new_from_stock("gtk-missing-image",Gtk.IconSize.MENU)
        
        self.set_lips()

        self.set_eyes()

        self.set_advice()


        self.w_cam = int(round(self.get_screen().get_width()/5*4))
        self.h_cam = self.get_screen().get_height()

        w_pan = int(round(self.get_screen().get_width()/5*1))
        h_pan = int(round(self.get_screen().get_height()/5*1))

        mbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing = 40)
        mbox.pack_start(self.eyesButton, False, False, 0)
        mbox.pack_start(self.lipsButton, False, False, 0)
        mbox.pack_start(self.adButton, False, False, 0)

        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing = 30)
        hbox.pack_start(self.mirror, False, False, 0)
        hbox.pack_start(mbox, True, True, 0)

        self.add(hbox)

        self.set_faceProcessor()

        

    def set_lips(self):
        self.lipsIcon = Gtk.Image()
        self.lipsIcon.set_from_file("resources/images/red_lips_icon.png")
        self.lipsButton = Gtk.Button()
        self.lipsButton.set_image(self.lipsIcon)
        self.lipsButton.connect("clicked", self.on_lips_click)

        self.lipsColorChooser = ColorPalette(lipstickPalette)

        self.lipsButtonPopover = Gtk.Popover()
        self.lipsButtonPopover.add(self.lipsColorChooser)
        self.lipsButtonPopover.set_position(Gtk.PositionType.BOTTOM)

    def on_lips_click(self, button):
        self.lipsButtonPopover.set_relative_to(button)
        self.lipsButtonPopover.show_all()
        self.lipsButtonPopover.popup()

    def set_eyes(self):
        self.eyesIcon = Gtk.Image()
        self.eyesIcon.set_from_file("resources/images/eye_icon.png")
        self.eyesButton = Gtk.Button()
        self.eyesButton.set_image(self.eyesIcon)
        self.eyesButton.connect("clicked", self.on_eyes_click)

        self.eyesColorChooser = ColorPalette(eyePalette)

        self.eyesButtonPopover = Gtk.Popover()
        self.eyesButtonPopover.add(self.eyesColorChooser)
        self.eyesButtonPopover.set_position(Gtk.PositionType.BOTTOM)

    def on_eyes_click(self, button):
        self.eyesButtonPopover.set_relative_to(button)
        self.eyesButtonPopover.show_all()
        self.eyesButtonPopover.popup()

    def set_advice(self):
        self.adIcon = Gtk.Image()
        self.adIcon.set_from_file("resources/images/lucky_icon.png")
        self.adButton = Gtk.Button()
        self.adButton.set_image(self.adIcon)
        self.adButton.connect("clicked", self.on_ad_click)

        adColorChooser = Gtk.ColorChooserWidget()

        self.adButtonPopover = Gtk.Popover()
        self.adButtonPopover.add(adColorChooser)
        self.adButtonPopover.set_position(Gtk.PositionType.BOTTOM)

    def on_ad_click(self, button):
        self.adButtonPopover.set_relative_to(button)
        self.adButtonPopover.show_all()
        self.adButtonPopover.popup()

    def set_faceProcessor(self):
        ap = argparse.ArgumentParser()
        ap.add_argument('-p', '--shape-predictor', dest='shape_predictor', required=True,help='path to facial landmark predictor')
        ap.add_argument('-s', '--source', dest='source',type=int, default=0, help='device index')
        ap.add_argument('-a', '--alpha', dest='alpha', type=float, default=0.25, help='alpha')
        args = ap.parse_args()
        self.detector = FacePartsDetector(args.shape_predictor, ['mouth', 'right_eye', 'left_eye', 'right_eyebrow', 'left_eyebrow', 'nose', 'jaw'])
        self.mouth_drawer = drw.MouthDrawer()
        self.eyes_drawer = drw.EyesDrawer()
        self.skin_color = features.SkinColorFeature()
        self.qr_code = features.QRCodeFeature()


    def show_frame(self, *args):
        x=0
        y=0
        ret, frame = cap.read()

        
        frame = imutils.resize(frame, width=700)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
        shapes = self.detector.detect(gray)
        self.skin_color.get(frame, shapes)
        self.qr_code.get(frame, shapes)
        eyes_sel_color = self.eyesColorChooser.get_sel_color()
        if len(eyes_sel_color)>0:
            self.eyes_drawer.draw(frame, shapes, (eyes_sel_color[2], eyes_sel_color[1], eyes_sel_color[0]), 0.3)
        lips_sel_color = self.lipsColorChooser.get_sel_color()
        if len(lips_sel_color)>0:
            self.mouth_drawer.draw(frame, shapes, ( lips_sel_color[2], lips_sel_color[1],  lips_sel_color[0]), 0.4)




        height, width, channels = frame.shape
        h = self.h_cam/height
        frame = cv2.resize(frame, None, fx=h, fy=h, interpolation = cv2.INTER_CUBIC)
        height, width, channels = frame.shape
        x=int(round((width-self.w_cam)/2))
        frame = frame[y:y+self.h_cam, x:x+self.w_cam]

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        pb = GdkPixbuf.Pixbuf.new_from_data(frame.tostring(),
                                            GdkPixbuf.Colorspace.RGB,
                                            False,
                                            8,
                                            frame.shape[1],
                                            frame.shape[0],
                                            frame.shape[2]*frame.shape[1])
        self.mirror.set_from_pixbuf(pb.copy())

        return True

cap = cv2.VideoCapture(0)

