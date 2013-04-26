import wx
import numpy
import time
import random

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
        self.figure = Figure()
        self.axes = self.figure.add_subplot(111)
        self.canvas = FigureCanvas(self, -1, self.figure)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.canvas, 1, wx.LEFT | wx.TOP | wx.GROW)
        self.SetSizer(self.sizer)
        self.Fit()

    def draw(self, obj1, obj2):
        for x in xrange(1,2):
            print "redraw"
            t = numpy.arange(0.0, 3.0, 0.01)
            t = t + self.shift
            s = numpy.sin(2 * numpy.pi * t)
            self.axes.plot(t, s)
            self.shift += 1
            time.sleep(1)

    # def animacja(self):
    #     for x in xrange(1,10):
    #         t = numpy.arange(0.0, 3.0, 0.01)
    #         s = numpy.sin(2 * numpy.pi * t * x)
    #         self.axes.plot(t, s)
    #         wx.Yield()
    #         self.Refresh()
    #         print "updated"
    #         time.sleep(1)

    def BufferFromVector(self, vector, width=300, height=10):
        (block_width, block_height) = ((width / len(vector)), height)
        canvas = numpy.empty((height,width, 4), numpy.uint8)
        CLR_FRAME = [0,0,0,255]
        CLR_UP    = [255,0,0,255]
        CLR_DOWN  = [0,255,0,255]
        canvas[:,:,:] = CLR_DOWN

        for i in xrange(len(vector)):
            block_start = i * block_width
            block_end = (i+1)*block_width
            if vector[i] == SPIN_UP:
                for x in xrange(block_start, block_end):
                    canvas[:,x,:] = CLR_UP
            canvas[:,block_start,:] = CLR_FRAME
        canvas[:,-1,:]=CLR_FRAME
        canvas[0, :,:]=CLR_FRAME
        canvas[-1,:,:]=CLR_FRAME
        return canvas

    def OnPaint(self, event):
        w, h = self.GetClientSizeTuple()
        arr = [0,0,0,0]
        self.__Buffer = self.BufferFromVector(
                vector=arr,
                width=(len(arr)*10),
                height=10
            )
        bitmap = wx.BitmapFromBufferRGBA(40, 10,self.__Buffer)
        dc = wx.BufferedPaintDC(self, buffer=bitmap)

    def OnQuitApp(self, event):
        self.Close()

    def startVizualization(self, event):
        self.algorithmA(self.printToBuffer)

    def printToBuffer(self, canvas):
        if self.__Buffer == []:
            self.__Buffer = self.BufferFromVector(
                vector=canvas[0],
                width=(len(canvas[0])*10),
                height=10
            )
            self.OnPaint(None)
        else:
            False
            # self.__Buffer = numpy.append(
            #     self.__Buffer,
            #     self.BufferFromVector(
            #         vector=canvas[0],
            #         width=(len(canvas[0])*10),
            #         height=10 ),
            #     axis=0
            # )

    def algorithmA(self, lambda_print_to):

        self.OnPaint(None)

        # arr = [[0,0,0,0,0,0,0,0,0,0]]
        # for x in xrange(1,10):
        #     arr.append([random.randrange(0, 2) for _ in range(0, 10)])
        #     lambda_print_to(arr)
        #     return False
