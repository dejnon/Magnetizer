import wx
import numpy

SPIN_UP = 1
SPIN_DOWN = 0

class Visualization(wx.Panel):
    def __init__(self, *args, **kwargs):
        wx.Panel.__init__(self, *args, **kwargs)
        self.Bind(wx.EVT_BUTTON, self.OnQuitApp, id=wx.ID_EXIT)
        self.Bind(wx.EVT_PAINT, self.OnPaint)

    def BitmapFromVector(self, vector, width=300, height=10):
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
        canvas[0,:,:]=CLR_FRAME
        canvas[-1,:,:]=CLR_FRAME
        return wx.BitmapFromBufferRGBA(width, height, canvas)

    def OnPaint(self, event):
        w, h = self.GetClientSizeTuple()
        v = [0,1,0,1,1,1,1,1,1,0,0,0,0,1,0,1,0]
        arr = self.BitmapFromVector(vector=v,width=(len(v)*10),height=10)
        v = [0,1,0,1,1,1,1,1,1,0,0,0,0,1,0,1,1]
        arr = self.BitmapFromVector(vector=v,width=(len(v)*10),height=10)
        dc = wx.BufferedPaintDC(self, buffer=arr)

    def OnQuitApp(self, event):
        self.Close()
