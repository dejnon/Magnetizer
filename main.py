import os, sys, inspect

import wx

from application.MainWindow import MainWindow

if __name__ == '__main__':
    app = wx.App(False)
    win = MainWindow()
    win.Show()
    app.MainLoop()
