import os, sys, inspect
# # realpath() with make your script run, even if you symlink it :)
# cmd_folder = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ))[0]))
# if cmd_folder not in sys.path:
#   sys.path.insert(0, cmd_folder)

# # use this if you want to include modules from a subforder
# cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"subfolder")))
# if cmd_subfolder not in sys.path:
#   sys.path.insert(0, cmd_subfolder)

import wx

from application.MainWindow import MainWindow

if __name__ == '__main__':
    app = wx.App(False)
    win = MainWindow(None)
    app.MainLoop()
