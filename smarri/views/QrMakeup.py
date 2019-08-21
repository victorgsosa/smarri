import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GObject
from views.ColorPalette import ColorPalette




class QrMakeup(Gtk.Button, GObject.GObject):
	

	def __init__(self):
		super().__init__()
		self.icon = Gtk.Image()
		self.set_opacity(0)

	def set_product_detection(self,value):
		if value=="eyes":
			self.icon.set_from_file("resources/images/eyeshadow.png")
		else:
			self.icon.set_from_file("resources/images/lipstick_qr.png")
		self.set_image(self.icon)
		self.set_opacity(1)

	def hide(self):
		self.set_opacity(0)



GObject.type_register(QrMakeup)



