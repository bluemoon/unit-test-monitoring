#!/usr/bin/env python
import os
import sys

from pyinotify   import *
from subprocess  import PIPE, Popen, call
from optparse    import OptionParser

import time
import gc
import dbus

global options

DEFAULT_CMD = "nosetests"

parser = OptionParser()
parser.add_option("--directory",    action="store",  dest="directory", default=DEFAULT_CMD)
parser.add_option("--cmd",    action="store",  dest="cmd", default=DEFAULT_CMD)
parser.add_option("--applet", action="store_true", dest="applet", default=False)
parser.add_option("--applet_debug", action="store_true", dest="applet_debug", default=False)
options, args = parser.parse_args()


class Monitoring(ProcessEvent):
    def my_init(self, options=None):
        self.cmd    = options.cmd
        self.applet = options.applet            
            
    def process_IN_MODIFY(self, event):
        # We have explicitely registered for this kind of event.
        filename = event.name.split('.')
        file_ext = filename[-1]

        if file_ext == 'rst' or file_ext == 'py': 
            print 'File modified "%s" ' % (event.name),
            
            #cmd = 'sphinx-build -b html . build'
            #print 'sphinx return value: ',
            retVal = Popen(self.cmd, shell=True, stderr=PIPE, stdout=PIPE)
            retVal.wait()


            if retVal.returncode != 0:
                print retVal.communicate()
            else:
                print retVal.returncode
            
            f_handle = file('applet-notify.log', 'a')
            f_handle.write(repr(retVal.returncode) + '\n')
            f_handle.flush()
            f_handle.close()

                
            f_handle = file('notify.log', 'a')
            f_handle.write(repr(event) + '\n')
            f_handle.flush()
            f_handle.close()
            
            self.last_call = time.time()


    def process_default(self, event):
        print 'default: ', event.maskname



class main:
    def main(self):
        if options.applet:
            print "Running Gnome applet."
            #os.fork()

            from gnome_notification import MonitorTray
            MonitorTray(os.getcwd())

        print '==> monitoring %s (type ^c to exit)' % os.getcwd()
        handler = Monitoring(options=options)
        wm = WatchManager()
        notifier = Notifier(wm, default_proc_fun=handler)
        ## rec is recursive and we want that set
        wm.add_watch('.', IN_MODIFY, rec=True)
        #wm.add_watch('../', IN_MODIFY, rec=True)
        notifier.loop()

if __name__ == "__main__":
    main_c = main()
    main_c.main()

