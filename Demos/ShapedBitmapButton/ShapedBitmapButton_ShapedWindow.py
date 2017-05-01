#!/usr/bin/env python
# -*- coding: utf-8 -*-

#-Imports-----------------------------------------------------------------------

#--Python Imports.
import os
import sys

#--wxPython Imports.
import wx
PHOENIX = 'phoenix' in wx.version()

try:  # Locally
    import mcow.shapedbitmapbutton as SBB
except ImportError:  # wxPython library
    import wx.lib.mcow.shapedbitmapbutton as SBB

__wxPyDemoPanel__ = 'TestPanel'
#-Globals-----------------------------------------------------------------------
gFileDir = os.path.dirname(os.path.abspath(__file__))
gImgDir = gFileDir + os.sep + 'bitmaps'


class ShapedBitmapButtonFrame(wx.Frame):
    def __init__(self, parent, log):
        self.log = log
        wx.Frame.__init__(self, parent, -1, "Shaped Window",
                         style = wx.FRAME_SHAPED
                         | wx.FRAME_NO_TASKBAR
                         | wx.STAY_ON_TOP
                         )

        self.hasShape = False
        self.delta = (0,0)

        self.Bind(wx.EVT_LEFT_DCLICK, self.OnDoubleClick)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        self.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)
        self.Bind(wx.EVT_MOTION, self.OnMouseMove)
        self.Bind(wx.EVT_RIGHT_UP, self.OnExit)
        self.Bind(wx.EVT_PAINT, self.OnPaint)

        self.bmp = wx.Bitmap(gImgDir + os.sep + 'shapedframe.png', wx.BITMAP_TYPE_PNG)
        w, h = self.bmp.GetWidth(), self.bmp.GetHeight()
        self.SetClientSize( (w, h) )

        if wx.Platform != "__WXMAC__":
            # wxMac clips the tooltip to the window shape, YUCK!!!
            self.SetToolTip(wx.ToolTip("Right-click to close the window\n"
                            "Double-click the image to set/unset the window shape"))

        if wx.Platform == "__WXGTK__":
            # wxGTK requires that the window be created before you can
            # set its shape, so delay the call to SetWindowShape until
            # this event.
            self.Bind(wx.EVT_WINDOW_CREATE, self.SetWindowShape)
        else:
            # On wxMSW and wxMac the window has already been created, so go for it.
            self.SetWindowShape()

        dc = wx.ClientDC(self)
        dc.DrawBitmap(self.bmp, 0,0, True)


        #----- Start ShapedBitmapButton Stuff -----#

        bmp1 = wx.Bitmap(gImgDir + os.sep + 'shapedbutton-normal64x40.png')
        bmp2 = wx.Bitmap(gImgDir + os.sep + 'shapedbutton-pressed64x40.png')
        bmp3 = wx.Bitmap(gImgDir + os.sep + 'shapedbutton-hover64x40.png')

        sbbtn1 = SBB.ShapedBitmapButton(self, -1,
            bitmap=bmp1,
            pressedBmp=bmp2,
            hoverBmp=bmp3,
            disabledBmp=None,
            parentBgBmp=self.bmp,
            pos=(104, 10))

        img1 = wx.Image(gImgDir + os.sep + 'shapedbutton-hover64x40.png').Rotate90().Mirror(True)
        img2 = wx.Image(gImgDir + os.sep + 'shapedbutton-normal64x40.png').Rotate90().Mirror(True)
        img3 = wx.Image(gImgDir + os.sep + 'shapedbutton-pressed64x40.png').Rotate90().Mirror(True)
        bmp1 = img1.ConvertToBitmap()
        bmp2 = img2.ConvertToBitmap()
        bmp3 = img3.ConvertToBitmap()

        sbbtn2 = SBB.ShapedBitmapButton(self, -1,
            bitmap=bmp1,
            pressedBmp=bmp2,
            hoverBmp=bmp3,
            disabledBmp=None,
            parentBgBmp=self.bmp,
            pos=(10, 104))

        sbbtn3 = SBB.ShapedBitmapButton(self, -1,
            bitmap=wx.Bitmap(gImgDir + os.sep + 'bigcheck128.png'),
            pressedBmp=wx.Bitmap(gImgDir + os.sep + 'bigcheck128-pressed.png'),
            hoverBmp=wx.Bitmap(gImgDir + os.sep + 'bigcheck128-hover.png'),
            disabledBmp=wx.Bitmap(gImgDir + os.sep + 'bigcheck128-disabled.png'),
            parentBgBmp=self.bmp,
            pos=(48, 200),
            # style=wx.BORDER_SIMPLE | wx.WANTS_CHARS
            )

        sbbtn4 = SBB.ShapedBitmapButton(self, -1,
            bitmap=wx.Bitmap(gImgDir + os.sep + 'shapedbutton-normal.png'),
            pressedBmp=wx.Bitmap(gImgDir + os.sep + 'shapedbutton-pressed.png'),
            hoverBmp=wx.Bitmap(gImgDir + os.sep + 'shapedbutton-hover.png'),
            disabledBmp=wx.Bitmap(gImgDir + os.sep + 'shapedbutton-disabled.png'),
            parentBgBmp=self.bmp,
            label='New Widget',
            # labelColour=wx.WHITE,
            labelRotation=27.0, labelPosition=(4, 68),
            labelFont=wx.Font(11, wx.FONTFAMILY_DEFAULT,
                                  wx.FONTSTYLE_NORMAL,
                                  wx.FONTWEIGHT_BOLD),
            pos=(192, 200),
            # style=wx.BORDER_SIMPLE
            )
        sbbtn4.SetToolTip(wx.ToolTip('This is a ShapedBitmapButton.'))

        sbbtn4.Bind(wx.EVT_TIMER, self.OnTimer)
        sbbtn4.timer = wx.Timer(sbbtn4)
        sbbtn4.timer.Start(500) # Every half a second.

        sbbtn5 = SBB.ShapedBitmapButton(self, wx.ID_CLOSE,
            bitmap=wx.Bitmap(gImgDir + os.sep + 'bigx128.png'),
            pressedBmp=wx.Bitmap(gImgDir + os.sep + 'bigx128-pressed.png'),
            hoverBmp=wx.Bitmap(gImgDir + os.sep + 'bigx128-hover.png'),
            disabledBmp=wx.Bitmap(gImgDir + os.sep + 'bigx128-disabled.png'),
            parentBgBmp=self.bmp,
            pos=(336, 200),
            # style=wx.BORDER_SIMPLE
            )

        sbbtn6 = SBB.ShapedBitmapButton(self, -1,
            bitmap=wx.Bitmap(gImgDir + os.sep + 'shapedbitmapbutton_text_normal.png'),
            pressedBmp=wx.Bitmap(gImgDir + os.sep + 'shapedbitmapbutton_text_pressed.png'),
            hoverBmp=wx.Bitmap(gImgDir + os.sep + 'shapedbitmapbutton_text_hover.png'),
            parentBgBmp=self.bmp,
            pos=(176, 68),
            # style=wx.BORDER_SIMPLE
            )

        # Lets bind all the ShapedBitmapButtons.
        for child in self.GetChildren():
            child.Bind(wx.EVT_BUTTON, self.OnButton)
        self.Centre()

    def OnTimer(self, event):
        evtObj = event.GetEventObject()
        evtObj.SetLabelEnabled(not evtObj.GetLabelEnabled())
        evtObj.Refresh()

    def OnButton(self, event):
        evtId = event.GetId()
        try:
            self.log.write('You Clicked Button with Id %s' % evtId)
        except Exception:
            print('You Clicked Button with Id %s' % evtId)
        if evtId == wx.ID_CLOSE:
            self.OnExit(None)
    #----- End ShapedBitmapButton Stuff -----#

    def SetWindowShape(self, *event):
        # Use the bitmap's mask to determine the region
        if PHOENIX:
            r = wx.Region(self.bmp, transColour=wx.Colour(255, 255, 255, 0), tolerance=0)
        else:
            self.bmp
            mask = wx.Mask(self.bmp, wx.Colour(255, 255, 255, 0))
            self.bmp.SetMask(mask)
            r = wx.RegionFromBitmap(self.bmp)
        self.hasShape = self.SetShape(r)

    def OnDoubleClick(self, event):
        if self.hasShape:
            self.SetShape(wx.Region())
            self.hasShape = False
        else:
            self.SetWindowShape()

    def OnPaint(self, event):
        dc = wx.PaintDC(self)
        dc.DrawBitmap(self.bmp, 0,0, True)

    def OnExit(self, event):
        self.Close()

    def OnLeftDown(self, event):
        self.CaptureMouse()
        x, y = self.ClientToScreen(event.GetPosition())
        originx, originy = self.GetPosition()
        dx = x - originx
        dy = y - originy
        self.delta = ((dx, dy))

    def OnLeftUp(self, event):
        if self.HasCapture():
            self.ReleaseMouse()

    def OnMouseMove(self, event):
        if event.Dragging() and event.LeftIsDown():
            x, y = self.ClientToScreen(event.GetPosition())
            fp = (x - self.delta[0], y - self.delta[1])
            self.Move(fp)


#- __main__ Demo ---------------------------------------------------------------


class ShapedBitmapButtonApp(wx.App):
    def OnInit(self):
        gMainWin = ShapedBitmapButtonFrame(None)
        gMainWin.SetTitle('ShapedBitmapButton ShapedFrame Demo')
        gMainWin.Show(True)

        return True


#- wxPython Demo ---------------------------------------------------------------


class TestPanel(wx.Panel):
    def __init__(self, parent, log):
        self.log = log
        wx.Panel.__init__(self, parent, -1)

        b = wx.Button(self, -1, "Show the ShapedWindow ShapedBitmapButton sample", (50,50))
        self.Bind(wx.EVT_BUTTON, self.OnButton, b)


    def OnButton(self, event):
        win = ShapedBitmapButtonFrame(self, self.log)
        win.Show(True)


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
