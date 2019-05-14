import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class ColorPaletteLine(Gtk.Box):

	def __init__(self, buttons):
		super().__init__(orientation=Gtk.Orientation.HORIZONTAL, spacing = 5)
		for x in buttons:
			self.pack_start(x, False, False, 0)