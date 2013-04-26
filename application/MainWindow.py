import time
import wx
from wx.lib.delayedresult import startWorker
import array
import numpy
import thread
import wx.lib.plot as plot


from application.Visualization import Visualization

class MainWindow(wx.Frame):

    def __init__(self, parent):
        wx.Frame.__init__(self, parent, 1, "Magnetizer", wx.DefaultPosition, size=(600, 400))
        self.draw()

    def draw(self):
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
        # OPTIONS
        updatingOptions = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(updatingOptions)

        # self.label = wx.StaticText(self, label="Ready")
        # updatingOptions.Add(self.label)

        # self.btn = wx.Button(self, label="Start")
        # updatingOptions.Add(self.btn)
        # self.btn.Bind(wx.EVT_BUTTON, self.onButton)

        # self.gauge = wx.Gauge(self)
        # updatingOptions.Add(self.gauge)

        # self.visualization = Visualization(self)
        # updatingOptions.Add(self.visualization)

        # self.btn_start = wx.Button(self, label="START VISUALIZATION")
        # updatingOptions.Add(self.btn_start)
        # self.btn_start.Bind(wx.EVT_BUTTON, self.longVizualization)


        Button1 = wx.Button(self, -1, "Update", (200,220))
        Button1.Bind(wx.EVT_BUTTON, self.redraw)

        plotter = plot.PlotCanvas(self)
        plotter.SetInitialSize(size=(500, 200))

        data = [[1, 10], [2, 5], [3, 10], [4, 5]]
        line = plot.PolyLine(data, colour='red', width=1)

        gc = plot.PlotGraphics([line], 'Test', 'x', 'y')
        plotter.Draw(gc)

    def redraw(self, event):
        plotter = plot.PlotCanvas(self)
        plotter.SetInitialSize(size=(500, 200))

        data2 = [[1, 20], [2, 15], [3, 20], [4, -10]]
        line = plot.PolyLine(data2, colour='red', width=1)

        gc = plot.PlotGraphics([line], 'Test', 'x', 'y')
        plotter.Draw(gc)

    def longVizualization(self, event):
        thread.start_new_thread(self.visualization.draw, (self, self))
        wx.Yield()

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
        time.sleep(1)
        wx.CallAfter(self.gauge.SetValue, 20)
        time.sleep(2)
        wx.CallAfter(self.gauge.SetValue, 50)
        time.sleep(1)
        wx.CallAfter(self.gauge.SetValue, 70)
        time.sleep(2)
        wx.CallAfter(self.onLongRunDone)
