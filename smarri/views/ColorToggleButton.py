import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk


class ColorToggleButton(Gtk.ToggleButton):

	def __init__(self,name,color):
		super().__init__()
		self.name=name
		da=Gtk.DrawingArea()
		da.set_size_request(24,24)
		da.connect("draw",self.on_draw)
		self.add(da)
		self.color = color

	def on_draw(self,widget,cr):
		width = widget.get_allocated_width()
		height = widget.get_allocated_height()
		cr.set_source_rgba(self.color[0]/255, self.color[1]/255, self.color[2]/255,1);
		cr.rectangle(0, 0, width, height)
		cr.fill()
		return False

	def get_name(self):
		return self.name