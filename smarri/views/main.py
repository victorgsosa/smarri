import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GLib, GdkPixbuf
import cv2
import numpy as np
from views.ColorPalette import ColorPalette
from views.RecommendationChooser import RecommendationChooser

import argparse
import imutils
import drawers as drw
import recommenders
import recommenders.features as features

from detector import FacePartsDetector


eyePalette = {'ecolor1': [77,0,0,0.1],
             'ecolor2': [103,4,34,0.1],
             'ecolor3': [133,4,56,0.1],
             'ecolor4': [64,3,62,0.1],
             'ecolor5': [5,0,58,0.1],
             'ecolor6': [178,216,216,0.05],
             'ecolor7': [102,178,178,0.05],
             'ecolor8': [0,128,128,0.05],
             'ecolor9': [0,102,102,0.1],
             'ecolor10': [0,76,76,0.1],
             'ecolor11': [141,85,36,0.1],
             'ecolor12': [198,134,66,0.05],
             'ecolor13': [224,172,105,0.05],
             'ecolor14': [241,194,125,0.05],
             'ecolor15': [255,219,172,0.05]}

lipstickPalette = {'lcolor1': [249,135,135,0.2],
             'lcolor2': [231,106,106,0.2],
             'lcolor3': [214,91,91,0.2],
             'lcolor4': [193,75,75,0.2],
             'lcolor5': [184,63,63,0.2],
             'lcolor6': [249,21,21,0.2],
             'lcolor7': [208,9,9,0.2],
             'lcolor8': [150,16,16,0.2],
             'lcolor9': [171,0,0,0.2],
             'lcolor10': [105,0,0,0.2]}

recBlanco= {'rec1':{'eyes':[103,4,34,0.1],'lips':[249,135,135,0.2]},
            'rec2':{'eyes':[102,178,178,0.05],'lips':[105,0,0,0.2]},
            'rec3':{'eyes':[141,85,36,0.1],'lips':[231,106,106,0.2]}}

recMestizo= {'rec1':{'eyes':[133,4,56,0.1],'lips':[171,0,0,0.2]},
             'rec2':{'eyes':[178,216,216,0.05],'lips':[214,91,91,0.2]},
             'rec3':{'eyes':[198,134,66,0.05],'lips':[150,16,16,0.2]}}

recNegro= { 'rec1':{'eyes':[64,3,62,0.1],'lips':[193,75,75,0.2]},
            'rec2':{'eyes':[0,128,128,0.05],'lips':[208,9,9,0.2]},
            'rec3':{'eyes':[255,219,172,0.05],'lips':[184,63,63,0.2]}}


SKIN_COLORS = {
    0: { 'mouth': [[0, 255, 0], [12,67,34], [255, 230, 156]], 'eyes': [[0, 255, 0], [12,67,34], [255, 230, 156]], 'skinColor':'Blanco' },
    1: { 'mouth': [[0, 0, 255], [12,255,34], [255, 230, 156]], 'eyes': [[0, 0, 255], [12,255,34], [255, 230, 156]],'skinColor':'Mestizo' },
    2: { 'mouth': [[255,0 , 0], [12,67,34], [255, 100, 156]], 'eyes': [[255,0 , 0], [12,67,34], [255, 100, 156]], 'skinColor':'Negro' }
}

QR_CODE_COLORS = {
    '0000001': {'mouth': [[249,135,135,0.2]],'color':'lcolor1'},
    '0000002': {'mouth': [[231,106,106,0.2]],'color':'lcolor2'},
    '0000003': {'mouth': [[214,91,91,0.2]],'color':'lcolor3'},
    '0000004': {'mouth': [[193,75,75,0.2]],'color':'lcolor4'},
    '0000005': {'mouth': [[184,63,63,0.2]],'color':'lcolor5'},
    '0000006': {'eyes': [[77,0,0,0.1]],'color':'ecolor1'},
    '0000007': {'eyes': [[64,3,62,0.1]],'color':'ecolor4'},
    '0000008': {'eyes': [[178,216,216,0.05]],'color':'ecolor6'},
    '0000009': {'eyes': [[0,102,102,0.1]],'color':'ecolor9'},
    '0000010': {'eyes': [[0,76,76,0.1]],'color':'ecolor10'},
}


class MainWindow(Gtk.Window):

    def __init__(self):
        
        Gtk.Window.__init__(self, title="Smart Make Up Mirror")
        #screen_width=self.get_screen().get_width()
        #screen_height=self.get_screen().get_height()
        screen_width=800
        screen_height=600


        self.set_border_width(10)
        self.set_size_request(screen_width,screen_height)

        self.mirror = Gtk.Image.new_from_stock("gtk-missing-image",Gtk.IconSize.MENU)
        self.set_lips()
        self.set_eyes()
        self.set_advice()


        self.w_cam = int(round(screen_width/5*4))
        self.h_cam = screen_height

        w_pan = int(round(screen_width/5*1))
        h_pan = int(round(screen_height/5*1))

        self.qrLabel=Gtk.Label()

        mbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing = 40)
        mbox.pack_start(self.eyesButton, False, False, 0)
        mbox.pack_start(self.lipsButton, False, False, 0)
        mbox.pack_start(self.adButton, False, False, 0)
        mbox.pack_start(self.qrLabel, False, False, 0)

        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing = 30)
        hbox.pack_start(self.mirror, False, False, 0)
        hbox.pack_start(mbox, True, True, 0)

        self.add(hbox)
        self.set_faceProcessor()

        self.eyes_sel_color = []
        self.lips_sel_color = []

        

    def set_lips(self):
        self.lipsIcon = Gtk.Image()
        self.lipsIcon.set_from_file("resources/images/red_lips_icon.png")
        self.lipsButton = Gtk.Button()
        self.lipsButton.set_image(self.lipsIcon)
        self.lipsButton.connect("clicked", self.on_lips_click)

        self.lipsColorChooser = ColorPalette(lipstickPalette)
        self.lipsColorChooser.connect("colorSelected", self.on_lipsColorSelected)

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
        self.eyesColorChooser.connect("colorSelected", self.on_eyesColorSelected)

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
        self.adButton.connect("clicked", self.on_advice_click)

        self.adChooser1 = RecommendationChooser(recBlanco,"Clara")
        self.adChooser2 = RecommendationChooser(recMestizo,"Media")
        self.adChooser3 = RecommendationChooser(recNegro,"Oscura")
        self.adChooser1.connect("recSelected", self.on_recSelected)
        self.adChooser2.connect("recSelected", self.on_recSelected)
        self.adChooser3.connect("recSelected", self.on_recSelected)

        self.vBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing = 5)

        self.adButtonPopover = Gtk.Popover()
        self.adButtonPopover.add(self.vBox)
        self.adButtonPopover.set_position(Gtk.PositionType.BOTTOM)

    def on_advice_click(self, button):
        if "skinColor" in self.skin_predict[0]:
            if self.vBox.get_center_widget()!=None:
                self.vBox.remove(self.vBox.get_center_widget())

            if self.skin_predict[0]["skinColor"]=="Blanco":
                self.vBox.set_center_widget(self.adChooser1)
            elif self.skin_predict[0]["skinColor"]=="Mestizo":
                self.vBox.set_center_widget(self.adChooser2)
            else:
                self.vBox.set_center_widget(self.adChooser3)
        

        self.adButtonPopover.set_relative_to(button)
        self.adButtonPopover.show_all()
        self.adButtonPopover.popup()
    
    def on_recSelected(self,widget,e_r,e_g,e_b,e_a,l_r,l_g,l_b,l_a):
        self.eyes_sel_color = []
        self.lips_sel_color = []
        self.eyes_sel_color.append(e_r)
        self.eyes_sel_color.append(e_g)
        self.eyes_sel_color.append(e_b)
        self.eyes_sel_color.append(e_a)
        self.lips_sel_color.append(l_r)
        self.lips_sel_color.append(l_g)
        self.lips_sel_color.append(l_b)
        self.lips_sel_color.append(l_a)
        print("alpha",e_a)
        print("alpha",l_a)
        self.clear_qrPanel()

    def on_eyesColorSelected(self,widget,e_r,e_g,e_b,e_a):
        self.eyes_sel_color = []
        self.eyes_sel_color.append(e_r)
        self.eyes_sel_color.append(e_g)
        self.eyes_sel_color.append(e_b)
        self.eyes_sel_color.append(e_a)
        print("alpha",e_a)
        self.clear_qrPanel()

    def on_lipsColorSelected(self,widget,l_r,l_g,l_b,l_a):
        self.lips_sel_color = []
        self.lips_sel_color.append(l_r)
        self.lips_sel_color.append(l_g)
        self.lips_sel_color.append(l_b)
        self.lips_sel_color.append(l_a)
        print("alpha",l_a)
        self.clear_qrPanel()
    

    def set_faceProcessor(self):
        ap = argparse.ArgumentParser()
        ap.add_argument('-p', '--shape-predictor', dest='shape_predictor', required=True,help='path to facial landmark predictor')
        ap.add_argument('-s', '--source', dest='source',type=int, default=0, help='device index')
        ap.add_argument('-a', '--alpha', dest='alpha', type=float, default=0.25, help='alpha')
        args = ap.parse_args()
        self.detector = FacePartsDetector(args.shape_predictor, ['mouth', 'right_eye', 'left_eye', 'right_eyebrow', 'left_eyebrow', 'nose', 'jaw'])
        self.mouth_drawer = drw.MouthDrawer()
        self.eyes_drawer = drw.EyesDrawer()
        self.skin_color = features.SkinCategoryFeature()
        self.qr_code = features.QRCodeFeature()
        self.skin_rec = recommenders.DictRecommender(self.skin_color, SKIN_COLORS)
        self.qr_rec = recommenders.DictRecommender(self.qr_code, QR_CODE_COLORS)

    def qr_detected(self,facePart,rgba,color):
        if facePart == "eyes":
            self.eyes_sel_color = rgba
            self.eyesColorChooser.set_sel_color(color)
        else:
            self.lips_sel_color = rgba
            self.lipsColorChooser.set_sel_color(color)
        self.qrLabel.set_text("QR DETECTADO")



    def clear_qrPanel(self):
        self.qrLabel.set_text("")
            

    
    def show_frame(self, *args):
        x=0
        y=0
        ret, frame = cap.read()
        if frame is not None:

            frame = imutils.resize(frame, width=700)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
            shapes = self.detector.detect(gray)
            
            self.qr_predict=self.qr_rec.predict(frame, shapes)
            if len(self.qr_predict)>0:
                if "mouth" in self.qr_predict[0]:
                    self.qr_detected("mouth",self.qr_predict[0]["mouth"][0],self.qr_predict[0]["color"])
                elif "eyes" in self.qr_predict[0]:
                    self.qr_detected("eyes",self.qr_predict[0]["eyes"][0],self.qr_predict[0]["color"])





            self.skin_predict=self.skin_rec.predict(frame, shapes)

            if len(self.eyes_sel_color)>0:
                self.eyes_drawer.draw(frame, shapes, (self.eyes_sel_color[2], self.eyes_sel_color[1], self.eyes_sel_color[0]), self.eyes_sel_color[3])
            if len(self.lips_sel_color)>0:
                self.mouth_drawer.draw(frame, shapes, (self.lips_sel_color[2], self.lips_sel_color[1],  self.lips_sel_color[0]), self.lips_sel_color[3])




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

