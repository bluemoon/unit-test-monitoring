from distutils.core import setup
import glob
setup(name = "notifier",
      version = "1.0",
      data_files = [ ("share/notifier/icons", ['24-em-check.png','24-em-cross.png']) ],
      author='Alex Toney',
      author_email='toneyalex@gmail.com',
      url='',
      packages = ["gnome_notification"],
      package_dir={'gnome_notification': '.'},
      scripts=['test-notifier']
      )
