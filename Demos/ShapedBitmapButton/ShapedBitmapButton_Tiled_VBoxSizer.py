#!/usr/bin/env python
# -*- coding: utf-8 -*-

#-Imports-----------------------------------------------------------------------

#--Python Imports.
import os
import sys

#--wxPython Imports.
# import wxversion
# wxversion.select('2.8')
# wxversion.select('3.0.3-msw-phoenix')
import wx

try:  # Locally
    import mcow.shapedbitmapbutton as SBB
    from mcow.shapedbitmapbutton import ShapedBitmapButton
except ImportError:  # wxPython library
    import wx.lib.mcow.shapedbitmapbutton as SBB
    from wx.lib.mcow.shapedbitmapbutton import ShapedBitmapButton

__wxPyDemoPanel__ = 'TestPanel'
#-Globals-----------------------------------------------------------------------
gFileDir = os.path.dirname(os.path.abspath(__file__))
gImgDir = gFileDir + os.sep + 'bitmaps'


class ShapedBitmapButtonPanel0(wx.Panel):
    """Sizers Positioning of the ShapedBitmapButton with tiled seamless background bitmap."""
    def __init__(self, parent, id=wx.ID_ANY,
                 pos=wx.DefaultPosition, size=wx.DefaultSize,
                 style=wx.BORDER_SUNKEN, name='panel'):
        wx.Panel.__init__(self, parent, id, pos, size, style, name)

        # Drawing performance is faster with a tilable bitmap about
        # the same size as what you are going to tile(In this case, the panel).
        # It also helps to optimize the images(reduce size/retain quality)
        # with a application such as FileOptimizer
        ## bgBmp = wx.Bitmap(gImgDir + os.sep + 'seamless' + os.sep + 'metalgriddark46x24.png', wx.BITMAP_TYPE_PNG)
        bgBmp = wx.Bitmap(gImgDir + os.sep + 'seamless' + os.sep + 'metalgriddark506x264.png', wx.BITMAP_TYPE_PNG)
        self.backgroundBitmap = SBB.MakeDisplaySizeBackgroundBitmap(bgBmp)
        # Slight flicker is less noticable at the edge when resizing if you use
        # a colour used most/close in the bitmap.
        self.SetBackgroundColour('#2C2C2C')
        ## self.SetBackgroundColour(wx.BLACK)

        ## self.backgroundBitmap = wx.Bitmap(gImgDir + os.sep + 'seamless' + os.sep + 'transparentbackground32.png', wx.BITMAP_TYPE_PNG)
        ## self.SetBackgroundColour(wx.WHITE)

        s1, s2 = 32, 32
        img1 = wx.Image(gImgDir + os.sep + 'shapedbutton-normal.png').Rescale(s1, s2)
        img2 = wx.Image(gImgDir + os.sep + 'shapedbutton-pressed.png').Rescale(s1, s2)
        img3 = wx.Image(gImgDir + os.sep + 'shapedbutton-hover.png').Rescale(s1, s2)
        img4 = wx.Image(gImgDir + os.sep + 'shapedbutton-disabled.png').Rescale(s1, s2)
        bmp1 = img1.ConvertToBitmap()
        bmp2 = img2.ConvertToBitmap()
        bmp3 = img3.ConvertToBitmap()
        bmp4 = img4.ConvertToBitmap()

        self.Bind(wx.EVT_PAINT, self.OnPaint)

        p = 1
        b = 5
        flags = wx.ALL

        vbSizer = wx.BoxSizer(wx.VERTICAL)
        for i in range(7):
            btn = SBB.ShapedBitmapButton(self, -1,
                bitmap=bmp1,
                pressedBmp=bmp2,
                hoverBmp=bmp3,
                disabledBmp=bmp4,
                parentBgBmp=self.backgroundBitmap
                )
            btn.Bind(wx.EVT_BUTTON, self.OnToggleBackground)
            vbSizer.Add(btn, p, flags, b)

        self.SetSizer(vbSizer)

    ## Additionally reduce OnSize bg bmp flicker of the buttons while resizing. ####
        self.Bind(wx.EVT_SIZE, self.OnSize)                                     #
        self.SetDoubleBuffered(True)                                            #
                                                                                #
    def OnSize(self, event):                                                    #
        self.Layout()                                                           #
    ################################################################################

    def OnToggleBackground(self, event):
        """Toggle the backgroundBitmap"""
        if self.GetBackgroundColour() == wx.WHITE:
            bgBmp = wx.Bitmap(gImgDir + os.sep + 'seamless' + os.sep + 'metalgriddark506x264.png', wx.BITMAP_TYPE_PNG)
            self.SetBackgroundColour('#2C2C2C')
        else:
            bgBmp = wx.Bitmap(gImgDir + os.sep + 'seamless' + os.sep + 'transparentbackground32.png', wx.BITMAP_TYPE_PNG)
            self.SetBackgroundColour(wx.WHITE)
        self.backgroundBitmap = SBB.MakeDisplaySizeBackgroundBitmap(bgBmp)
        [child.SetParentBackgroundBitmap(self.backgroundBitmap)
            for child in self.GetChildren() if isinstance(child, SBB.ShapedBitmapButton)]
        self.Refresh()

    def OnPaint(self, event):
        dc = wx.BufferedPaintDC(self)
        dc.Clear()
        dc.DrawBitmap(self.backgroundBitmap, 0, 0, True)


class ShapedBitmapButtonFrame(wx.Frame):
    def __init__(self, parent, id=wx.ID_ANY, title=wx.EmptyString,
                 pos=wx.DefaultPosition, size=wx.DefaultSize,
                 style=wx.DEFAULT_FRAME_STYLE, name='frame'):
        wx.Frame.__init__(self, parent, id, title, pos, size, style, name)

        ## self.SetDoubleBuffered(True)
        self.CreateStatusBar()
        self.SetStatusText('wxPython %s' % wx.version())

        b = 5
        vbSizer = wx.BoxSizer(wx.VERTICAL)
        vbSizer.Add(ShapedBitmapButtonPanel0(self), 1, wx.EXPAND | wx.ALL, b)

        # self.SetSizerAndFit(vbSizer)
        self.SetSizer(vbSizer)
        self.Fit()

        self.Bind(wx.EVT_CLOSE, self.OnDestroy)

    def OnDestroy(self, event):
        self.Destroy()


#- __main__ Demo ---------------------------------------------------------------


class ShapedBitmapButtonApp(wx.App):
    def OnInit(self):
        gMainWin = ShapedBitmapButtonFrame(None)
        gMainWin.SetTitle('ShapedBitmapButton Demo')
        gMainWin.Show()

        return True


#- wxPython Demo ---------------------------------------------------------------


class TestPanel(wx.Panel):
    def __init__(self, parent, log):
        self.log = log
        wx.Panel.__init__(self, parent, -1)

        b = wx.Button(self, -1, 'Show ShapedBitmapButton Background VBoxSizer Demo', pos=(50, 50))
        b.Bind(wx.EVT_BUTTON, self.OnShowShapedBitmapButton)

    def OnShowShapedBitmapButton(self, event):
        gMainWin = ShapedBitmapButtonFrame(self)
        gMainWin.SetTitle('ShapedBitmapButton Demo %s' % gMainWin.GetSize())
        gMainWin.Show()


def runTest(frame, nb, log):
    win = TestPanel(nb, log)
    return win


#--DocUtils Imports.
try:
    from docutils.core import publish_string
    overview = publish_string(SBB.__doc__.replace(':class:', ''), writer_name='html')
except ImportError:
    overview = SBB.__doc__


#- __main__ --------------------------------------------------------------------


if __name__ == '__main__':
    import os
    import sys
    try: # Try running with wxPythonDemo run.py first.
        import run
        run.main(['', os.path.basename(sys.argv[0])] + sys.argv[1:])
    except ImportError: # run.py not found, try running normally.
        print(wx.version())
        gApp = ShapedBitmapButtonApp(redirect=False,
                filename=None,
                useBestVisual=False,
                clearSigInt=True)

        gApp.MainLoop()
