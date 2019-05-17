import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk


class RecommendationToggleButton(Gtk.ToggleButton):

	def __init__(self,name,eColor,lColor):
		super().__init__()
		
		self.name=name
		self.lcolor = lColor
		self.ecolor = eColor


		vBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing = 5)
		eBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing = 5)
		lBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing = 5)
		
		eLabel = Gtk.Label("Ojos")

		eda=Gtk.DrawingArea()
		eda.set_size_request(24,24)
		eda.connect("draw",self.on_edraw)

		eBox.pack_start(eLabel,False,False,0)
		eBox.pack_start(eda,False,False,0)

		lLabel = Gtk.Label("Labios")
		lda=Gtk.DrawingArea()
		lda.set_size_request(24,24)
		lda.connect("draw",self.on_ldraw)
		lBox.pack_start(lLabel,False,False,0)
		lBox.pack_start(lda,False,False,0)

		vBox.pack_start(eBox,False,False,0)
		vBox.pack_start(lBox,False,False,0)

		
		self.add(vBox)
		

	def on_edraw(self,widget,cr):
		width = widget.get_allocated_width()
		height = widget.get_allocated_height()
		cr.set_source_rgba(self.ecolor[0]/255, self.ecolor[1]/255, self.ecolor[2]/255,1);
		cr.rectangle(0, 0, width, height)
		cr.fill()
		return False

	def on_ldraw(self,widget,cr):
		width = widget.get_allocated_width()
		height = widget.get_allocated_height()
		cr.set_source_rgba(self.lcolor[0]/255, self.lcolor[1]/255, self.lcolor[2]/255,1);
		cr.rectangle(0, 0, width, height)
		cr.fill()
		return False

	def get_name(self):
		return self.name