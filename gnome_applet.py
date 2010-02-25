#!/usr/bin/env python
import os
import pygtk

pygtk.require('2.0')

import gtk 
import gobject
import gnome
import gnomeapplet
import gc

class testMonitoringApplet(gnomeapplet.Applet):
    def __init__(self, applet, iid):
        self.__gobject_init__()
        self.applet = applet

        self.timeout = 5000

        self.good_icon_path = "/home/bluemoon/Projects/nose_monitoring/24-em-check.png"
        self.bad_icon_path  = "/home/bluemoon/Projects/nose_monitoring/24-em-cross.png"

        
        self.create_applet()

        self.timeout_source = gobject.timeout_add(1000, self.timeout_callback)
            
        applet.connect("destroy", self.cleanup)
        applet.show_all()

    def change_orientation(self,arg1,data):
        pass

        
    def create_applet(self):
        self.create_icon()
        self.applet.show_all()

    def cleanup(self):
        pass


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
        size = self.applet.get_size() - 2
        self.icon = gtk.Image()
        self.icon.set_from_image(self.good_icon_path)
        self.applet.add(self.icon)

        #self.icon.set_from_file(self.good_icon_path)
        #self.icon.show()
        

    def set_icon(self, path):
        self.icon.clear()
        gc.collect()
        
        self.icon.set_from_file(path)



gobject.type_register(testMonitoringApplet)
    
    
if __name__ == "__main__":
    if False:
        main_window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        main_window.set_title("Python Applet")
        main_window.connect("destroy", gtk.mainquit) 
        main_window.set_default_size(36, 36)
        
        app = gnomeapplet.Applet()
        testMonitoring_factory(app, None)
        app.reparent(main_window)
        
        main_window.show_all()
        
        gtk.main()
        sys.exit()

    gnomeapplet.bonobo_factory(
        "OAFIID:GNOME_testMonitoring_factory",
        testMonitoringApplet.__gtype__,
        "Python applet example",
        "0.1",
        testMonitoring_factory
        )

