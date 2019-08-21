import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GObject
from views.ColorPalette import ColorPalette


lipstickPalette = {'lcolor1': [249,135,135,0.15],
             'lcolor2': [231,106,106,0.15],
             'lcolor3': [214,91,91,0.15],
             'lcolor4': [193,75,75,0.2],
             'lcolor5': [184,63,63,0.2],
             'lcolor6': [249,21,21,0.2],
             'lcolor7': [208,9,9,0.2],
             'lcolor8': [150,16,16,0.2],
             'lcolor9': [171,0,0,0.2],
             'lcolor10': [105,0,0,0.2]}


class LipsMakeup(Gtk.Button, GObject.GObject):

	__gsignals__ = {
        'manualMakeup': (GObject.SIGNAL_RUN_FIRST, None,
                      ())
    }

	def __init__(self):
		super().__init__()
		self.lips_sel_color = []
		self.lipsIcon = Gtk.Image()
		self.lipsIcon.set_from_file("resources/images/red_lips_icon.png")
		self.set_image(self.lipsIcon)
		self.connect("clicked", self.on_lips_click)
		self.set_opacity(0.3)

		self.lipsColorChooser = ColorPalette(lipstickPalette)
		self.lipsColorChooser.connect("colorSelected", self.on_lipsColorSelected)

		self.lipsButtonPopover = Gtk.Popover()
		self.lipsButtonPopover.add(self.lipsColorChooser)
		self.lipsButtonPopover.set_position(Gtk.PositionType.BOTTOM)

	def on_lips_click(self, button):
		self.lipsButtonPopover.set_relative_to(button)
		self.lipsButtonPopover.show_all()
		self.lipsButtonPopover.popup()
	
	def on_lipsColorSelected(self,widget,l_r,l_g,l_b,l_a):
		self.lips_sel_color = []
		self.lips_sel_color.append(l_r)
		self.lips_sel_color.append(l_g)
		self.lips_sel_color.append(l_b)
		self.lips_sel_color.append(l_a)
		self.emit("manualMakeup")


	def get_lips_sel_color(self):
		return self.lips_sel_color

	def set_lipsMakeup(self,rgba,color):
		self.lips_sel_color = rgba
		self.lipsColorChooser.set_sel_color(color)

	def reset(self):
		self.lipsColorChooser.reset_palette()
		self.lips_sel_color = []


GObject.type_register(LipsMakeup)



