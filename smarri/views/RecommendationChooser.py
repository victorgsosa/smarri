import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GObject


from views.RecommendationToggleButton import RecommendationToggleButton


class RecommendationChooser(Gtk.Box, GObject.GObject):

	__gsignals__ = {
        'recSelected': (GObject.SIGNAL_RUN_FIRST, None,
                      (int,int,int,float,int,int,int,float,))
    }

	def __init__(self,recommendation,name):
		super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing = 5)
		self.label = Gtk.Label("Recomendaciones piel: "+name)
		self.pack_start(self.label,False, False, 0)

		self.recommendation = recommendation

		self.button1 = RecommendationToggleButton("rec1",recommendation["rec1"]["eyes"],recommendation["rec1"]["lips"])
		self.button2 = RecommendationToggleButton("rec2",recommendation["rec2"]["eyes"],recommendation["rec2"]["lips"])
		self.button3 = RecommendationToggleButton("rec3",recommendation["rec3"]["eyes"],recommendation["rec3"]["lips"])
		self.button1.connect("toggled", self.on_button_toggled, "rec1")
		self.button2.connect("toggled", self.on_button_toggled, "rec2")
		self.button3.connect("toggled", self.on_button_toggled, "rec3")

		hBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing = 5)
		hBox.pack_start(self.button1,False,False,0)
		hBox.pack_start(self.button2,False,False,0)
		hBox.pack_start(self.button3,False,False,0)

		self.pack_start(hBox,False, False, 0)
		

	def on_button_toggled(self, button, name):
		if button.get_active():
			self.selectedButton = button.get_name()
			if self.selectedButton=="rec1":
				self.button2.set_active(False)
				self.button3.set_active(False)
				self.sel_eColor = self.recommendation["rec1"]["eyes"]
				self.sel_lColor = self.recommendation["rec1"]["lips"]
			elif self.selectedButton=="rec2":
				self.button1.set_active(False)
				self.button3.set_active(False)
				self.sel_eColor = self.recommendation["rec2"]["eyes"]
				self.sel_lColor = self.recommendation["rec2"]["lips"]
			else:
				self.button2.set_active(False)
				self.button1.set_active(False)
				self.sel_eColor = self.recommendation["rec3"]["eyes"]
				self.sel_lColor = self.recommendation["rec3"]["lips"]
			self.emit("recSelected",self.sel_eColor[0],self.sel_eColor[1],self.sel_eColor[2],self.sel_eColor[3],self.sel_lColor[0],self.sel_lColor[1],self.sel_lColor[2],self.sel_lColor[3])
					 
	
	def get_sel_eColor(self):
		return self.sel_eColor

	def get_sel_lColor(self):
		return self.sel_lColor

	def reset_recommendation(self):
		self.button1.set_active(False)
		self.button2.set_active(False)
		self.button3.set_active(False)

		
GObject.type_register(RecommendationChooser)


