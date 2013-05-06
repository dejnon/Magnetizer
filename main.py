import os
import pprint
import random
import sys
import wx

# The recommended way to use wx with mpl is with the WXAgg
# backend.
#
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
        # wx.Frame.__init__(self, None, -1, self.title)
        wx.Frame.__init__(self, None, -1, self.title, size=(950,590))

        self.datagen = DataGen()
        self.data = [self.datagen.next()]
        self.paused = True

        self.create_menu()          # +shortcuts
        self.create_status_bar()    # line at the bottom

        # self.main_panel = wx.Panel(self)
        self.MainGrid = wx.FlexGridSizer( 2, 2, 0, 0 )
        self.create_canvas()        # "the drawing place"
        # self.create_control_panel() # switches and toggles
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

    def create_canvas(self):
        self.init_plot()
        # self.canvas = FigCanvas(self.MainGrid , -1, self.fig)

        # self.figure = pylab.figure(figsize = (8.4,4.1))
        # self.subplot = self.figure.add_subplot(1,1,1)
        # self.subplot.axes.get_xaxis().set_visible(False)
        # self.subplot.axes.get_yaxis().set_visible(False)
        # self.figure.tight_layout()
        # self.canvas = FigCanvas(self, -1, self.fig)


    def draw_interface(self):
        self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
        self.MainGrid.SetFlexibleDirection( wx.BOTH )
        self.MainGrid.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
        Plot = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"Plot" ), wx.VERTICAL )
        Plot.SetMinSize( wx.Size( 400,200 ) )
        self.plot_sizer = wx.BoxSizer(wx.VERTICAL)
        self.plot_sizer.Add(self.canvas, 1, wx.EXPAND | wx.ALL)
        Plot.Add( self.plot_sizer, 0, wx.ALL, 5 )
        self.MainGrid.Add( Plot, 1, wx.ALIGN_LEFT|wx.ALIGN_TOP, 5 )
        Updatable = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"Updating" ), wx.VERTICAL )
        Update = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"UpdateMode" ), wx.VERTICAL )
        self.Sequential = wx.RadioButton( self, wx.ID_ANY, u"Sequential", wx.DefaultPosition, wx.DefaultSize, 0 )
        Update.Add( self.Sequential, 0, wx.ALL, 5 )
        self.Synchronous = wx.RadioButton( self, wx.ID_ANY, u"Synchronous", wx.DefaultPosition, wx.DefaultSize, 0 )
        Update.Add( self.Synchronous, 0, wx.ALL, 5 )
        self.CSequential = wx.RadioButton( self, wx.ID_ANY, u"CSequential", wx.DefaultPosition, wx.DefaultSize, 0 )
        Update.Add( self.CSequential, 0, wx.ALL, 5 )
        Updatable.Add( Update, 1, wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL, 5 )
        PlotView = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"Plot View" ), wx.VERTICAL )
        self.Follow = wx.RadioButton( self, wx.ID_ANY, u"Follow", wx.DefaultPosition, wx.DefaultSize, 0 )
        PlotView.Add( self.Follow, 0, wx.ALL, 5 )
        self.SeeAll = wx.RadioButton( self, wx.ID_ANY, u"See all", wx.DefaultPosition, wx.DefaultSize, 0 )
        PlotView.Add( self.SeeAll, 0, wx.ALL, 5 )
        Updatable.Add( PlotView, 1, wx.EXPAND, 5 )
        CLSize = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"cL" ), wx.VERTICAL )
        self.CL = wx.Slider( self, wx.ID_ANY, 50, 0, 100, wx.DefaultPosition, wx.DefaultSize, wx.SL_HORIZONTAL )
        CLSize.Add( self.CL, 0, wx.ALL, 5 )
        Updatable.Add( CLSize, 1, 0, 5 )
        WZero = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"W0" ), wx.VERTICAL )
        self.W0 = wx.TextCtrl( self, wx.ID_ANY, u"(cL/L)*i*1.0", wx.DefaultPosition, wx.DefaultSize, 0 )
        WZero.Add( self.W0, 0, wx.ALL, 5 )
        Updatable.Add( WZero, 1, wx.EXPAND, 5 )
        self.MainGrid.Add( Updatable, 1, wx.ALIGN_RIGHT|wx.ALIGN_TOP, 5 )
        Simulation = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"Simulation" ), wx.HORIZONTAL )
        StartConditions = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"Start conditions" ), wx.VERTICAL )
        self.Ferromagnet = wx.RadioButton( self, wx.ID_ANY, u"Ferromagnet", wx.DefaultPosition, wx.DefaultSize, 0 )
        StartConditions.Add( self.Ferromagnet, 0, wx.ALL, 5 )
        self.AntiFerromagnet = wx.RadioButton( self, wx.ID_ANY, u"Antiferromagnet", wx.DefaultPosition, wx.DefaultSize, 0 )
        StartConditions.Add( self.AntiFerromagnet, 0, wx.ALL, 5 )
        self.Random = wx.RadioButton( self, wx.ID_ANY, u"Random", wx.DefaultPosition, wx.DefaultSize, 0 )
        StartConditions.Add( self.Random, 0, wx.ALL, 5 )
        Simulation.Add( StartConditions, 1, wx.EXPAND, 5 )
        Boundaries = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"Boundaries" ), wx.VERTICAL )
        self.Cyclic = wx.RadioButton( self, wx.ID_ANY, u"Cyclic", wx.DefaultPosition, wx.DefaultSize, 0 )
        Boundaries.Add( self.Cyclic, 0, wx.ALL, 5 )
        self.Table = wx.RadioButton( self, wx.ID_ANY, u"Table", wx.DefaultPosition, wx.DefaultSize, 0 )
        Boundaries.Add( self.Table, 0, wx.ALL, 5 )
        Simulation.Add( Boundaries, 1, wx.EXPAND, 5 )
        TimeSteps = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"Time steps" ), wx.VERTICAL )
        self.Time = wx.TextCtrl( self, wx.ID_ANY, u"0", wx.DefaultPosition, wx.DefaultSize, 0 )
        TimeSteps.Add( self.Time, 0, wx.ALL, 5 )
        Simulation.Add( TimeSteps, 1, wx.EXPAND, 5 )
        StartStop = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"Start/Stop" ), wx.VERTICAL )
        self.Start = wx.Button(self, label="Start")
        self.Bind(wx.EVT_BUTTON, self.on_pause_button ,self.Start)
        StartStop.Add( self.Start, 0, wx.ALL, 5 )
        Simulation.Add( StartStop, 1, wx.EXPAND, 5 )
        self.MainGrid.Add( Simulation, 1, wx.ALIGN_BOTTOM|wx.ALIGN_LEFT, 5 )
        self.SetSizer( self.MainGrid )
        self.Layout()
        self.Centre( wx.BOTH )

    def init_plot(self):
        self.dpi = 100
        self.fig = Figure((6.7, 3.3), dpi=self.dpi)

        # self.axes = self.fig.add_subplot(111)

        # self.fig = pylab.figure(figsize = (8.4,4.1))
        self.axes = self.fig.add_subplot(1,1,1)
        self.axes.axes.get_xaxis().set_visible(False)
        self.axes.axes.get_yaxis().set_visible(False)
        self.fig.tight_layout()

        self.canvas = FigCanvas(self, -1, self.fig)

        # self.axes.set_axis_bgcolor('black')
        # self.axes.set_title('Very important random data', size=12)

        # pylab.setp(self.axes.get_xticklabels(), fontsize=8)
        # pylab.setp(self.axes.get_yticklabels(), fontsize=8)

        # plot the data as a line series, and save the reference
        # to the plotted line series
        #
        self.plot_data = self.axes.matshow(self.data, aspect='auto')
        # self.plot_data.set_data(self.init_data)
        # self.plot_data.set_data(self.data)

    def draw_plot(self):
        """ Redraws the plot
        """
        # when xmin is on auto, it "follows" xmax to produce a
        # sliding window effect. therefore, xmin is assigned after
        # xmax.
        #
        # if self.xmax_control.is_auto():
        #     xmax = len(self.data) if len(self.data) > 50 else 50
        # else:
        #     xmax = int(self.xmax_control.manual_value())

        # if self.xmin_control.is_auto():
        #     xmin = xmax - 50
        # else:
        #     xmin = int(self.xmin_control.manual_value())

        # for ymin and ymax, find the minimal and maximal values
        # in the data set and add a mininal margin.
        #
        # note that it's easy to change this scheme to the
        # minimal/maximal value in the current display, and not
        # the whole data set.
        #
        # if self.ymin_control.is_auto():
        #     ymin = round(min(self.data), 0) - 1
        # else:
        #     ymin = int(self.ymin_control.manual_value())

        # if self.ymax_control.is_auto():
        #     ymax = round(max(self.data), 0) + 1
        # else:
        #     ymax = int(self.ymax_control.manual_value())

        # self.axes.set_xbound(lower=xmin, upper=xmax)
        # self.axes.set_ybound(lower=ymin, upper=ymax)

        # anecdote: axes.grid assumes b=True if any other flag is
        # given even if b is set to False.
        # so just passing the flag into the first statement won't
        # work.
        #
        # if self.cb_grid.IsChecked():
        #     self.axes.grid(True, color='gray')
        # else:
        #     self.axes.grid(False)

        # Using setp here is convenient, because get_xticklabels
        # returns a list over which one needs to explicitly
        # iterate, and setp already handles this.
        #
        # pylab.setp(self.axes.get_xticklabels(),
        #     visible=self.cb_xlab.IsChecked())

        self.plot_data.set_data(self.data)
        # self.plot_data.set_xdata(np.arange(len(self.data)))
        # self.plot_data.set_ydata(np.array(self.data))

        self.canvas.draw()

    def on_pause_button(self, event):
        self.paused = not self.paused

    def on_update_pause_button(self, event):
        label = "Resume" if self.paused else "Pause"
        self.pause_button.SetLabel(label)

    def on_cb_grid(self, event):
        self.draw_plot()

    def on_cb_xlab(self, event):
        self.draw_plot()

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
        #
        if not self.paused:
            self.data.append(self.datagen.next())
            self.Time.SetValue(str(self.datagen.iterations))

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
    app = wx.PySimpleApp()
    app.frame = GraphFrame()
    app.frame.Show()
    app.MainLoop()
