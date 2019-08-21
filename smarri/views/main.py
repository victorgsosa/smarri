import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GLib, GdkPixbuf
import cv2
import numpy as np
from views.SideMenu import SideMenu
from views.EyesMakeup import EyesMakeup
from views.LipsMakeup import LipsMakeup
from views.SmartMakeup import SmartMakeup
from views.QrMakeup import QrMakeup

import imutils
import drawers as drw
import recommenders
import recommenders.features as features

from utils.decorators import timing
from utils.stream import RecommenderStream



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
    '0000006': {'eyes': [[185,118,132,0.1]],'color':'ecolor3'},
    '0000007': {'eyes': [[64,3,62,0.1]],'color':'ecolor4'},
    '0000008': {'eyes': [[178,216,216,0.05]],'color':'ecolor6'},
    '0000009': {'eyes': [[0,102,102,0.1]],'color':'ecolor9'},
    '0000010': {'eyes': [[0,76,76,0.1]],'color':'ecolor10'},
}


class MainWindow(Gtk.Window):

    def __init__(self, stream):
        
        Gtk.Window.__init__(self, title="Smart Make Up Mirror")
        #screen_width=self.get_screen().get_width()
        #screen_height=self.get_screen().get_height()
        screen_width=1280
        screen_height=720

        self.stream = stream
        self.set_border_width(10)
        self.set_size_request(screen_width,screen_height)

        self.sideMenu = SideMenu()
        self.sideMenu.connect("resetMakeup", self.on_reset)

        self.mirror = Gtk.Image.new_from_stock("gtk-missing-image",Gtk.IconSize.MENU)

        self.w_cam = int(round(screen_width/5*4))
        self.h_cam = screen_height

        w_pan = int(round(screen_width/5*1))
        h_pan = int(round(screen_height/5*1))

        self.eyesMakeup = EyesMakeup();
        self.eyesMakeup.connect("manualMakeup", self.on_manualSelection)
        self.lipsMakeup = LipsMakeup();
        self.lipsMakeup.connect("manualMakeup", self.on_manualSelection)
        self.smartMakeup = SmartMakeup();
        self.smartMakeup.connect("smartMakeup", self.on_smartSelection)
        self.qrMakeup = QrMakeup();
        self.sideMenu.add_widget(self.eyesMakeup)
        self.sideMenu.add_widget(self.lipsMakeup)
        self.sideMenu.add_widget(self.smartMakeup)
        self.sideMenu.add_widget(self.qrMakeup)

        overCont = Gtk.Overlay()
        overCont.add(self.mirror)
        overCont.add_overlay(self.sideMenu)

        self.add(overCont)
        self.set_faceProcessor()

        self.eyes_sel_color = []
        self.lips_sel_color = []
        self.smartSelection = False

    def on_reset(self,widget):
        print("reset")
        self.smartSelection = False
        self.eyesMakeup.reset()
        self.lipsMakeup.reset()
        self.smartMakeup.reset()
        self.qrMakeup.hide()
    
    def on_smartSelection(self,widget):
        self.smartSelection = True
        self.qrMakeup.hide()
        print("smart")

    def on_manualSelection(self,widget):
        self.smartSelection = False
        self.qrMakeup.hide()
        print("manual")

    def set_faceProcessor(self):
        self.mouth_drawer = drw.MouthDrawer()
        self.eyes_drawer = drw.EyesDrawer()
        self.skin_color = features.SkinCategoryFeature()
        self.qr_code = features.QRCodeFeature()
        skin_rec = recommenders.DictRecommender(self.skin_color, SKIN_COLORS)
        qr_rec = recommenders.DictRecommender(self.qr_code, QR_CODE_COLORS)
        self.skin_rec = RecommenderStream(self.stream, skin_rec).start()
        self.qr_rec = RecommenderStream(self.stream, qr_rec).start()

    def qr_detected(self,facePart,rgba,color):
        if facePart == "eyes":
            self.eyesMakeup.set_eyesMakeup(rgba,color)
            self.qrMakeup.set_product_detection("eyes")
        else:
            self.lipsMakeup.set_lipsMakeup(rgba,color)
            self.qrMakeup.set_product_detection("lips")
            

    @timing
    def show_frame(self, *args):
        x=0
        y=0
        frame, shapes = self.stream.read()
        if frame is not None:

            self.qr_predict=self.qr_rec.read()
            if len(self.qr_predict)>0:
                if "mouth" in self.qr_predict[0]:
                    self.qr_detected("mouth",self.qr_predict[0]["mouth"][0],self.qr_predict[0]["color"])
                elif "eyes" in self.qr_predict[0]:
                    self.qr_detected("eyes",self.qr_predict[0]["eyes"][0],self.qr_predict[0]["color"])
                
            self.smartMakeup.set_predict(self.skin_rec.read())

            if self.smartSelection:
                self.eyes_sel_color, self.lips_sel_color = self.smartMakeup.get_smart_makeup()
            else:
                self.eyes_sel_color = self.eyesMakeup.get_eyes_sel_color()
                self.lips_sel_color = self.lipsMakeup.get_lips_sel_color()
            
            if len(self.eyes_sel_color)>0:
                frame = self.eyes_drawer.draw(frame, shapes, (self.eyes_sel_color[2], self.eyes_sel_color[1], self.eyes_sel_color[0]), self.eyes_sel_color[3])
                        
            if len(self.lips_sel_color)>0:
                frame = self.mouth_drawer.draw(frame, shapes, (self.lips_sel_color[2], self.lips_sel_color[1],  self.lips_sel_color[0]), self.lips_sel_color[3])

            height, width, channels = frame.shape
            

            h = self.h_cam/height
            frame = cv2.resize(frame, None, fy = h, fx = h, interpolation = cv2.INTER_AREA )

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            pb = GdkPixbuf.Pixbuf.new_from_data(frame.tostring(),
                                                GdkPixbuf.Colorspace.RGB,
                                                False,
                                                8,
                                                width,
                                                height,
                                                channels*width)
            self.mirror.set_from_pixbuf(pb)

            return True


