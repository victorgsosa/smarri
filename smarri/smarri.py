import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib
from views.main import MainWindow


if __name__ == '__main__':
	smarry = MainWindow()
	smarry.connect("destroy", Gtk.main_quit)
	smarry.show_all()
	GLib.idle_add(smarry.show_frame)
	Gtk.main()