import os
import pprint
import random
import sys
import wx

import matplotlib
matplotlib.use('WXAgg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import \
    FigureCanvasWxAgg as FigCanvas, \
    NavigationToolbar2WxAgg as NavigationToolbar
import numpy as np
import pylab

from datagen import DataGen
from boundcontrolbox import BoundControlBox

class GraphFrame(wx.Frame):
    title = 'Magnetizr'
    def __init__(self):
        wx.Frame.__init__(self, None, -1, self.title, size=(950,590))

        self.datagen = DataGen()
        self.data = [self.datagen.next()]
        self.paused = True

        self.create_menu()          # +shortcuts
        self.create_status_bar()    # line at the bottom

        self.MainGrid = wx.FlexGridSizer( 2, 2, 0, 0 )
        self.init_plot()            # "the drawing place"
        self.draw_interface()

        self.redraw_timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.on_redraw_timer, self.redraw_timer)
        self.redraw_timer.Start(100)

    def create_menu(self):
        self.menubar = wx.MenuBar()
        menu_file = wx.Menu()
        m_expt = menu_file.Append(-1, "&Save plot\tCtrl-S", "Save plot to file")
        self.Bind(wx.EVT_MENU, self.on_save_plot, m_expt)
        menu_file.AppendSeparator()
        m_exit = menu_file.Append(-1, "E&xit\tCtrl-X", "Exit")
        self.Bind(wx.EVT_MENU, self.on_exit, m_exit)
        self.menubar.Append(menu_file, "&File")
        self.SetMenuBar(self.menubar)

    def create_status_bar(self):
        self.statusbar = self.CreateStatusBar()

    def update_mode(self, event):
        print "hello"

    def draw_interface(self):
        self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
        self.MainGrid.SetFlexibleDirection( wx.BOTH )
        self.MainGrid.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

        # PLOT
        Plot = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"Plot" ), wx.VERTICAL )
        Plot.SetMinSize( wx.Size( 400,200 ) )
        self.plot_sizer = wx.BoxSizer(wx.VERTICAL)
        self.plot_sizer.Add(self.canvas, 1, wx.EXPAND | wx.ALL)
        Plot.Add( self.plot_sizer, 0, wx.ALL, 5 )

        # UPDATABLE
        Updatable = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"Updating" ), wx.VERTICAL )
        #   Updating mode
        UpdateModes = ["Sequential", "Synchronous", "CSequential"]
        Update = wx.RadioBox(self, wx.ID_ANY, "Update Mode",  wx.DefaultPosition, wx.DefaultSize, UpdateModes, 1, wx.RA_SPECIFY_COLS)
        Updatable.Add( Update, 1, wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL, 5 )
        Update.Bind(wx.EVT_RADIOBUTTON, self.update_mode)
        #   Plot view
        PlotView = wx.RadioBox(self, wx.ID_ANY, "Plot view",  wx.DefaultPosition, wx.DefaultSize, ["Follow", "See all"], 1, wx.RA_SPECIFY_COLS)
        Updatable.Add( PlotView, 1, wx.EXPAND, 5 )
        #   CL size
        CLSize = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"cL" ), wx.VERTICAL )
        self.CL = wx.Slider( self, wx.ID_ANY, 50, 0, 100, wx.DefaultPosition, wx.DefaultSize, wx.SL_HORIZONTAL )
        CLSize.Add( self.CL, 0, wx.ALL, 5 )
        Updatable.Add( CLSize, 1, 0, 5 )
        #   W0
        WZero = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"W0" ), wx.VERTICAL )
        self.W0 = wx.TextCtrl( self, wx.ID_ANY, u"(cL/L)*i*1.0", wx.DefaultPosition, wx.DefaultSize, 0 )
        WZero.Add( self.W0, 0, wx.ALL, 5 )
        Updatable.Add( WZero, 1, wx.EXPAND, 5 )

        # SIMULATION CONTROLS
        Simulation = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"Simulation" ), wx.HORIZONTAL )
        #   Starting conditions
        StartConditions = wx.RadioBox(self, wx.ID_ANY, "Plot view",  wx.DefaultPosition, wx.DefaultSize, ["Ferromagnet", "Antiferromagnet", "Random"], 1, wx.RA_SPECIFY_COLS)
        Simulation.Add( StartConditions, 1, wx.EXPAND, 5 )
        #   Boundaries
        Boundaries = wx.RadioBox(self, wx.ID_ANY, "Plot view",  wx.DefaultPosition, wx.DefaultSize, ["Cyclic", "Sharp(table)"], 1, wx.RA_SPECIFY_COLS)
        Simulation.Add( Boundaries, 1, wx.EXPAND, 5 )
        #   Time steps
        TimeSteps = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"Time steps" ), wx.VERTICAL )
        self.Time = wx.TextCtrl( self, wx.ID_ANY, u"100", wx.DefaultPosition, wx.DefaultSize, 0 )
        TimeSteps.Add( self.Time, 0, wx.ALL, 5 )
        Simulation.Add( TimeSteps, 1, wx.EXPAND, 5 )
        #   Startstop
        StartStop = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"Start/Stop" ), wx.VERTICAL )
        self.StartStopBtn = wx.Button(self, label="Start")
        self.Bind(wx.EVT_BUTTON, self.on_pause_button ,self.StartStopBtn)
        StartStop.Add( self.StartStopBtn, 0, wx.ALL, 5 )
        Simulation.Add( StartStop, 1, wx.EXPAND, 5 )

        self.MainGrid.Add( Plot, 1, wx.ALIGN_LEFT|wx.ALIGN_TOP, 5 )
        self.MainGrid.Add( Updatable, 1, wx.ALIGN_RIGHT|wx.ALIGN_TOP, 5 )
        self.MainGrid.Add( Simulation, 1, wx.ALIGN_BOTTOM|wx.ALIGN_LEFT, 5 )

        self.SetSizer( self.MainGrid )
        self.Layout()
        self.Centre( wx.BOTH )

    def init_plot(self):
        self.dpi = 100
        self.fig = Figure((6.7, 3.3), dpi=self.dpi)
        self.axes = self.fig.add_subplot(1,1,1)
        self.axes.axes.get_xaxis().set_visible(False)
        self.axes.axes.get_yaxis().set_visible(False)
        self.fig.tight_layout()
        self.canvas = FigCanvas(self, -1, self.fig)
        self.plot_data = self.axes.matshow(self.data, aspect='auto')

    def draw_plot(self):
        self.plot_data.set_data(self.data)
        self.canvas.draw()

    def on_pause_button(self, event):
        self.paused = not self.paused
        label = "Start" if self.paused else "Stop"
        self.StartStopBtn.SetLabel(label)

    def on_save_plot(self, event):
        file_choices = "PNG (*.png)|*.png"

        dlg = wx.FileDialog(
            self,
            message="Save plot as...",
            defaultDir=os.getcwd(),
            defaultFile="plot.png",
            wildcard=file_choices,
            style=wx.SAVE)

        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            self.canvas.print_figure(path, dpi=self.dpi)
            self.flash_status_message("Saved to %s" % path)

    def on_redraw_timer(self, event):
        # if paused do not add data, but still redraw the plot
        # (to respond to scale modifications, grid change, etc.)
        if not self.paused:
            self.data.append(self.datagen.next())
            self.Time.SetValue(str(self.datagen.interations_left))
        if self.datagen.interations_left <= 0:
            self.paused = True
        self.draw_plot()

    def on_exit(self, event):
        self.Destroy()

    def flash_status_message(self, msg, flash_len_ms=1500):
        self.statusbar.SetStatusText(msg)
        self.timeroff = wx.Timer(self)
        self.Bind(
            wx.EVT_TIMER,
            self.on_flash_status_off,
            self.timeroff)
        self.timeroff.Start(flash_len_ms, oneShot=True)

    def on_flash_status_off(self, event):
        self.statusbar.SetStatusText('')

if __name__ == '__main__':
    app = wx.App()
    app.frame = GraphFrame()
    app.frame.Show()
    app.MainLoop()
