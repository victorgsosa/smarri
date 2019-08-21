import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GObject
from views.RecommendationChooser import RecommendationChooser

recBlanco= {'rec1':{'eyes':[185,118,132,0.1],'lips':[105,0,0,0.2]},
            'rec2':{'eyes':[64,3,62,0.1],'lips':[184,63,63,0.2]},
            'rec3':{'eyes':[0,102,102,0.1],'lips':[150,16,16,0.2]}}

recMestizo= {'rec1':{'eyes':[141,85,36,0.1],'lips':[150,16,16,0.2]},
             'rec2':{'eyes':[103,4,34,0.1],'lips':[249,21,21,0.2]},
             'rec3':{'eyes':[185,118,132,0.1],'lips':[193,75,75,0.2]}}

recNegro= { 'rec1':{'eyes':[178,216,216,0.05],'lips':[231,106,106,0.15]},
            'rec2':{'eyes':[224,172,105,0.05],'lips':[184,63,63,0.2]},
            'rec3':{'eyes':[103,4,34,0.1],'lips':[150,16,16,0.2]}}


class SmartMakeup(Gtk.Button, GObject.GObject):

	__gsignals__ = {
        'smartMakeup': (GObject.SIGNAL_RUN_FIRST, None,
                      ())
    }

	def __init__(self):
		super().__init__()
		self.skin_predict = []
		self.eyes_sel_color = []
		self.lips_sel_color = []
		self.adIcon = Gtk.Image()
		self.adIcon.set_from_file("resources/images/magic.png")
		self.set_image(self.adIcon)
		self.connect("clicked", self.on_advice_click)
		self.set_opacity(0.3)

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
	
	def on_lipsColorSelected(self,widget,l_r,l_g,l_b,l_a):
		self.lips_sel_color = []
		self.lips_sel_color.append(l_r)
		self.lips_sel_color.append(l_g)
		self.lips_sel_color.append(l_b)
		self.lips_sel_color.append(l_a)

	def set_predict(self,predict):
		self.skin_predict = predict

	def get_smart_makeup(self):
		return self.eyes_sel_color, self.lips_sel_color

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
		self.emit("smartMakeup")

	def reset(self):
		self.adChooser1.reset_recommendation()
		self.adChooser2.reset_recommendation()
		self.adChooser3.reset_recommendation()



GObject.type_register(SmartMakeup)



