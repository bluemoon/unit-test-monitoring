#!/usr/bin/python
import pygtk
pygtk.require('2.0')
import gtk
import gc
import gobject

class MonitorTray:
    def __init__(self, directory):
        self.timeout = 5000
        self.good_icon_path = "24-em-check.png"
        self.bad_icon_path  = "24-em-cross.png"
        self.directory = directory

        self.timeout_source = gobject.timeout_add(self.timeout, self.timeout_callback)
        self.create_applet()
        
    def create_applet(self):
        self.statusIcon = gtk.StatusIcon()
        self.create_icon()
        
        self.menu = gtk.Menu()
        self.menuItem = gtk.ImageMenuItem(gtk.STOCK_EXECUTE)
        self.menuItem.connect('activate', self.execute_cb, self.statusIcon)
        self.menu.append(self.menuItem)
        
        self.menuItem = gtk.ImageMenuItem(gtk.STOCK_QUIT)
        self.menuItem.connect('activate', self.quit_cb, self.statusIcon)
        self.menu.append(self.menuItem)
        
        self.statusIcon.connect('popup-menu', self.popup_menu_cb, self.menu)
        self.statusIcon.set_visible(1)
        
        gtk.main()


    def timeout_callback(self):
        f_handle = open('applet-notify.log', 'r')
        return_values = f_handle.readlines()
        last = return_values[-1]
        
        if int(last) != 0:
            self.set_icon(self.bad_icon_path)
        else:
            self.set_icon(self.good_icon_path)

        return 1

            
    def create_icon(self):
        self.statusIcon.set_from_file("24-em-check.png")
        self.statusIcon.set_visible(True)
        self.statusIcon.set_tooltip("Monitoring (%s)" % self.directory)

    def set_icon(self, path):
        #self.statusIcon.clear()
        #gc.collect()
        self.statusIcon.set_from_file(path)


    def execute_cb(self, widget, event, data = None):
        window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        window.set_border_width(10)
        
        button = gtk.Button("Hello World")
        button.connect_object("clicked", gtk.Widget.destroy, window)
        
        window.add(button)
        button.show()
        window.show()

    def quit_cb(self, widget, data = None):
        gtk.main_quit()

    def popup_menu_cb(self, widget, button, time, data = None):
            if button == 3:
                if data:
                    data.show_all()
                    data.popup(None, None, gtk.status_icon_position_menu,
                           3, time, self.statusIcon)

if __name__ == "__main__":
  tray = MonitorTray()
