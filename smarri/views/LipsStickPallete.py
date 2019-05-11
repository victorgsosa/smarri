import gi
gi.require_version('Gtk', '3.0')
from gi.repository import GObject, Gtk, Gdk


class LipsStickPallete(Gtk.Box, GObject.GObject, Gtk.ColorChooser):

	

	def __init__(self):
		self.hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing = 10)
		self.button = Gtk.Button()
		self.hbox.pack_start(self.button, True, True, 0)
		GObject.GObject.__init__(self)
		self.rgba = Gdk.RGBA.to_color(Gdk.RGBA(red=0, green=.33, blue=.66, alpha=1.0))
		self.use_alpha = Gtk.ColorChooser.use_alpha
		
	def do_add_palette(self,orientation,colors_per_line,colors):
		a = 1
	def do_get_rgba(self):
		return self.rgba

	def do_get_rgba(self,color):
		self.rgba = color

	def do_get_use_alpha(self):
		return self.use_alpha

	def do_set_use_alpha(self,use_alpha):
		self.use_alpha = use_alpha

		



