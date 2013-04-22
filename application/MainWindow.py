import time
import wx
from wx.lib.delayedresult import startWorker
import array
import numpy
import thread

from application.Visualization import Visualization

class MainWindow(wx.Frame):

    def __init__(self, parent):
        wx.Frame.__init__(self, parent)
        self.createMenu()
        self.drawInterface()
        self.bindings()
        self.Show()

    def createMenu(self):
        menubar = wx.MenuBar()
        file = wx.Menu()
        edit = wx.Menu()
        help = wx.Menu()
        file.AppendSeparator()
        quit = wx.MenuItem(file, 105, '&Quit\tCtrl+Q', 'Quit the Application', wx.ITEM_NORMAL)
        wx.EVT_MENU(self, 105, self.OnQuit )
        file.AppendItem(quit)
        menubar.Append(file, '&File')
        menubar.Append(edit, '&Edit')
        menubar.Append(help, '&Help')
        self.SetMenuBar(menubar)
        self.CreateStatusBar()

    def bindings(self):
        False
        # self.Bind(wx.EVT_BUTTON, self.OnQuitApp, id=wx.ID_EXIT)

    def OnQuit(self, event):
        self.Close()

    def drawInterface(self):
        self.label = wx.StaticText(self, label="Ready")
        self.btn = wx.Button(self, label="Start")
        self.gauge = wx.Gauge(self)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.label, proportion=1, flag=wx.EXPAND)
        sizer.Add(self.btn, proportion=0, flag=wx.EXPAND)
        sizer.Add(self.gauge, proportion=0, flag=wx.EXPAND)

        self.SetSizerAndFit(sizer)

        self.Bind(wx.EVT_BUTTON, self.onButton)
        # wx.Button(self, wx.ID_EXIT, 'Close', (50, 130))
        # self.panel = wx.Panel(self)
        # self.sizerPanel = wx.BoxSizer()
        # self.sizerPanel.Add(self.panel, proportion=1, flag=wx.EXPAND)
        # self.sizerMain = wx.BoxSizer()
        # self.drawingDB = Visualization(self.panel, size=(300, 300))
        # self.sizerMain.Add(self.drawingDB, 1, wx.ALL | wx.EXPAND, 5)
        # self.panel.SetSizerAndFit(self.sizerMain)
        # self.SetSizerAndFit(self.sizerPanel)

    def onButton(self, evt):
        self.btn.Enable(False)
        self.gauge.SetValue(0)
        self.label.SetLabel("Running")
        thread.start_new_thread(self.longRunning, ())

    def onLongRunDone(self):
        self.gauge.SetValue(100)
        self.label.SetLabel("Done")
        self.btn.Enable(True)

    def longRunning(self):
        """This runs in a different thread.  Sleep is used to simulate a long running task."""
        time.sleep(3)
        wx.CallAfter(self.gauge.SetValue, 20)
        time.sleep(5)
        wx.CallAfter(self.gauge.SetValue, 50)
        time.sleep(1)
        wx.CallAfter(self.gauge.SetValue, 70)
        time.sleep(10)
        wx.CallAfter(self.onLongRunDone)
