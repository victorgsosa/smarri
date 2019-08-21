import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GObject
from views.ColorPalette import ColorPalette


eyePalette = {'ecolor1': [77,0,0,0.1],
             'ecolor2': [103,4,34,0.1],
             'ecolor3': [185,118,132,0.1],
             'ecolor4': [64,3,62,0.1],
             'ecolor5': [5,0,58,0.1],
             'ecolor6': [178,216,216,0.05],
             'ecolor7': [102,178,178,0.05],
             'ecolor8': [0,128,128,0.05],
             'ecolor9': [0,102,102,0.1],
             'ecolor10': [0,76,76,0.1],
             'ecolor11': [141,85,36,0.1],
             'ecolor12': [198,134,66,0.05],
             'ecolor13': [224,172,105,0.05],
             'ecolor14': [241,194,125,0.05],
             'ecolor15': [255,219,172,0.05]}


class EyesMakeup(Gtk.Button, GObject.GObject):
	__gsignals__ = {
        'manualMakeup': (GObject.SIGNAL_RUN_FIRST, None,
                      ())
    }

	def __init__(self):
		super().__init__()
		self.eyes_sel_color = []
		self.eyesIcon = Gtk.Image()
		self.eyesIcon.set_from_file("resources/images/eye_icon.png")
		self.set_image(self.eyesIcon)
		self.connect("clicked", self.on_eyes_click)
		self.set_opacity(0.3)

		self.eyesColorChooser = ColorPalette(eyePalette)
		self.eyesColorChooser.connect("colorSelected", self.on_eyesColorSelected)

		self.eyesButtonPopover = Gtk.Popover()
		self.eyesButtonPopover.add(self.eyesColorChooser)
		self.eyesButtonPopover.set_position(Gtk.PositionType.BOTTOM)

	def on_eyes_click(self, button):
		self.eyesButtonPopover.set_relative_to(button)
		self.eyesButtonPopover.show_all()
		self.eyesButtonPopover.popup()

	def on_eyesColorSelected(self,widget,e_r,e_g,e_b,e_a):
		self.eyes_sel_color = []
		self.eyes_sel_color.append(e_r)
		self.eyes_sel_color.append(e_g)
		self.eyes_sel_color.append(e_b)
		self.eyes_sel_color.append(e_a)
		self.emit("manualMakeup")
	
	def get_eyes_sel_color(self):
		return self.eyes_sel_color

	def set_eyesMakeup(self,rgba,color):
		self.eyes_sel_color = rgba
		self.eyesColorChooser.set_sel_color(color)

	def reset(self):
		self.eyesColorChooser.reset_palette()
		self.eyes_sel_color = []


GObject.type_register(EyesMakeup)



