import wx
import numpy
import time
import random
import wx.lib.plot as plot

import matplotlib
matplotlib.use('WXAgg')

from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wx import NavigationToolbar2Wx
from matplotlib.figure import Figure

SPIN_UP = 1
SPIN_DOWN = 0

class Visualization(wx.Panel):
    __Buffer = [] # BufferedImage
    __Canvas = [] # canvas[y,x,colors]
    shift = 1

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        plotter = plot.PlotCanvas(self)
        plotter.SetInitialSize(size=(500, 200))

        data = [[1, 10], [2, 5], [3, 10], [4, 5]]
        line = plot.PolyLine(data, colour='red', width=1)

        gc = plot.PlotGraphics([line], 'Test', 'x', 'y')
        plotter.Draw(gc)
        # self.figure = Figure()
        # self.axes = self.figure.add_subplot(111)
        # self.canvas = FigureCanvas(self, -1, self.figure)
        # self.sizer = wx.BoxSizer(wx.VERTICAL)
        # self.sizer.Add(self.canvas, 1, wx.LEFT | wx.TOP | wx.GROW)
        # self.SetSizer(self.sizer)
        # self.Fit()


    def startVizualization(self):
        plotter = plot.PlotCanvas(self)
        plotter.SetInitialSize(size=(500, 200))

        data2 = [[1, 20], [2, 15], [3, 20], [4, -10]]
        line = plot.PolyLine(data2, colour='red', width=1)

        gc = plot.PlotGraphics([line], 'Test', 'x', 'y')
        plotter.Draw(gc)

    def redraw(self, event):
        plotter = plot.PlotCanvas(self)
        plotter.SetInitialSize(size=(500, 200))

        data2 = [[1, 20], [2, 15], [3, 20], [4, -10]]
        line = plot.PolyLine(data2, colour='red', width=1)

        gc = plot.PlotGraphics([line], 'Test', 'x', 'y')
        plotter.Draw(gc)
