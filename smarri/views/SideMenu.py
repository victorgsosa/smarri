import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GObject




class SideMenu(Gtk.Box, GObject.GObject):
	__gsignals__ = {
        'resetMakeup': (GObject.SIGNAL_RUN_FIRST, None,
                      ())
    }

	def __init__(self):
		super().__init__(orientation=Gtk.Orientation.HORIZONTAL, spacing = 30)
		self.eBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing = 5)
		self.iBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing = 20)
		self.expanded = False

		self.hamIcon = Gtk.Image()
		self.hamIcon.set_from_file("resources/images/hamburger_icon2.png")
		self.but=Gtk.Button()
		self.but.set_image(self.hamIcon)
		self.but.set_size_request(50,50)
		self.but.connect("clicked", self.on_toggle)
		self.but.set_opacity(0.3)

		self.clearIcon = Gtk.Image()
		self.clearIcon.set_from_file("resources/images/facewash.png")
		self.clear=Gtk.Button()
		self.clear.set_image(self.clearIcon)
		self.clear.set_size_request(50,50)
		self.clear.connect("clicked", self.on_clear)
		self.clear.set_opacity(0.4)

		self.invFrame=Gtk.Frame()
		self.invFrame.set_size_request(50,600)
		self.invFrame.set_shadow_type(Gtk.ShadowType.NONE)

		self.eBox.pack_start(self.but,False,False,0)
		self.eBox.pack_start(self.clear,False,False,0)
		self.eBox.pack_start(self.invFrame,False,False,0)

		self.mainFrame=Gtk.Frame()
		self.mainFrame.set_size_request(1180,600)
		self.mainFrame.set_shadow_type(Gtk.ShadowType.NONE)
		self.pack_start(self.mainFrame, False, False, 0)

		self.pack_start(self.eBox,False,False,0)
		self.pack_start(self.iBox,False,False,0) 
        
	def add_widget(self, widget):
		self.iBox.pack_start(widget,False,False,0)

	def on_toggle(self, button):
		if self.expanded:
			self.mainFrame.set_size_request(1180,600)
		else:
			self.mainFrame.set_size_request(1000,600)
		self.expanded = not self.expanded

	def on_clear(self, button):
		self.emit("resetMakeup")

GObject.type_register(SideMenu)



