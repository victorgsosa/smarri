import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from views.ColorToggleButton import ColorToggleButton
from views.ColorPaletteLine import ColorPaletteLine



class ColorPalette(Gtk.Box):

	def __init__(self, palette):
		super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing = 5)
		self.palette = palette
		self.selectedColor = []
		self.buttons=[]
		cont = 1
		line = []
		for key, value in self.palette.items():
			lbl = key
			button = ColorToggleButton(lbl,value)
			button.connect("toggled", self.on_button_toggled, lbl)
			self.buttons.append(button)
			line.append(button)
			if cont%5 == 0:
				self.pack_start(ColorPaletteLine(line), False, False, 0)
				line=[]
			cont = cont + 1
		if len(line)>0:
			self.pack_start(ColorPaletteLine(line), False, False, 0)

			
		

	def on_button_toggled(self, button, name):
		if button.get_active():
			self.selectedColor = self.palette[button.get_name()]
			#print("selected", self.selectedColor)	
			for x in self.buttons:
				if x.get_name() != button.get_name():
					print("X", x.get_name(), "button", button.get_name())
					x.set_active(False) 
	
	def get_sel_color(self):
		return self.selectedColor
		



