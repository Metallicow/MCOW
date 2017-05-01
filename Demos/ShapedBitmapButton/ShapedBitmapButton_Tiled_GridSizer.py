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
from wx.lib.embeddedimage import PyEmbeddedImage


try:  # Locally
    import mcow.shapedbitmapbutton as SBB
except ImportError:  # wxPython library
    import wx.lib.mcow.shapedbitmapbutton as SBB

__wxPyDemoPanel__ = 'TestPanel'
#-Globals-----------------------------------------------------------------------
gFileDir = os.path.dirname(os.path.abspath(__file__))
gImgDir = gFileDir + os.sep + 'bitmaps'


# seamless = PyEmbeddedImage(
#     "iVBORw0KGgoAAAANSUhEUgAAADAAAAAwCAAAAAByaaZbAAAAQ0lEQVR42u2QoQ0AMAzDjIbG"
#     "hsby/5Wrqh4QvhgZWkYNu8BxdAuxCsvRKUTjOH7MuB8z7seM51Iu5VIu5VIu5dLHlx5Ir44B"
#     "+hbgrgAAAABJRU5ErkJggg==")

seamless = PyEmbeddedImage(
    "iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAAAAABWESUoAAAAIElEQVR4AWP4DwVnoACdP1IU"
    "oEug80eIgtH0MJoekPkA0wuWLp08mZwAAAAASUVORK5CYII=")

shapedbitmapbutton_normal = PyEmbeddedImage(
    "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"
    "SUVORK5CYII=")

shapedbitmapbutton_hover = PyEmbeddedImage(
    "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")

shapedbitmapbutton_pressed = PyEmbeddedImage(
    "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")


class ShapedBitmapButtonPanel8(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent, -1)

        self.backgroundBitmap = SBB.MakeDisplaySizeBackgroundBitmap(seamless.GetBitmap())

        gSizer = wx.GridSizer(rows=2, cols=3, vgap=15, hgap=15)

        for i in range(3):
            sButton = SBB.ShapedBitmapButton(self, -1,
                bitmap=shapedbitmapbutton_normal.GetBitmap(),
                pressedBmp=shapedbitmapbutton_pressed.GetBitmap(),
                hoverBmp=shapedbitmapbutton_hover.GetBitmap(),
                parentBgBmp=self.backgroundBitmap,
                label='Undo', labelForeColour=wx.WHITE,
                labelRotation=27.0, labelPosition=(2, 14),
                labelFont=wx.Font(11, wx.FONTFAMILY_DEFAULT,
                                     wx.FONTSTYLE_NORMAL,
                                     wx.FONTWEIGHT_BOLD),
                # style=wx.BORDER_SIMPLE # Show the Rect
                    # | wx.WANTS_CHARS # Don't Eat Enter/Return Key
                    )

            # sButton = wx.Button(self, -1, 'Button %s' % i, style=wx.BORDER_SIMPLE|wx.WANTS_CHARS)
            if i == 1:
                sButton.Rotate180()
                sButton.SetLabel('Redo')
                sButton.SetLabelPosition((20, 22))
            if i == 2:
                sButton.SetLabel('Timer')
                sButton.SetLabelPosition((2, 16))

            sButton.Bind(wx.EVT_BUTTON, self.OnButton)
            sButton.Bind(wx.EVT_RIGHT_UP, self.OnRightUp)
            gSizer.Add(sButton, 0, wx.ALIGN_CENTER | wx.ALL, 15)

        sButton.Bind(wx.EVT_TIMER, self.OnTimer)
        sButton.timer = wx.Timer(sButton)
        sButton.timer.Start(500)  # Every half a second.

        for i in range(3):
            sButton = SBB.ShapedBitmapButton(self, -1,
                bitmap=shapedbitmapbutton_normal.GetBitmap(),
                pressedBmp=shapedbitmapbutton_pressed.GetBitmap(),
                hoverBmp=shapedbitmapbutton_hover.GetBitmap(),
                parentBgBmp=self.backgroundBitmap,
                # style=wx.BORDER_SIMPLE # Show the Rect
                    # | wx.WANTS_CHARS # Don't Eat Enter/Return Key
                    )

            if i == 0:
                sButton.Mirror()
            if i == 1:
                sButton.Rotate90()
            if i == 2:
                sButton.SetToolTip(wx.ToolTip('I have a ToolTip!'))

            sButton.Bind(wx.EVT_BUTTON, self.OnButton)
            sButton.Bind(wx.EVT_RIGHT_UP, self.OnRightUp)
            gSizer.Add(sButton, 0, wx.ALIGN_CENTER | wx.ALL, 15)

        self.SetSizer(gSizer)
        self.Fit()
        # self.SetAutoLayout(True)

        # wx.CallAfter(sButton.SetSize, (32, 128))

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)

    def OnTimer(self, event):
        print('OnTimer')
        event.Skip()
        evtObj = event.GetEventObject()
        print(not evtObj.GetLabelEnabled())
        evtObj.SetLabelEnabled(not evtObj.GetLabelEnabled())
        evtObj.Update()
        evtObj.Refresh()

    def OnRightUp(self, event):
        print('OnRightUp')

    def OnButton(self, event):
        print('wxPython Rocks!')

    def OnEraseBackground(self, event):
        pass

    def OnPaint(self, event):
        dc = wx.BufferedPaintDC(self)
        dc.Clear()
        dc.DrawBitmap(self.backgroundBitmap, 0, 0, True)


class ShapedBitmapButtonFrame(wx.Frame):
    def __init__(self, parent, id=wx.ID_ANY, title=wx.EmptyString,
                 pos=wx.DefaultPosition, size=wx.DefaultSize,
                 style=wx.DEFAULT_FRAME_STYLE, name='frame'):
        wx.Frame.__init__(self, parent, id, title, pos, size, style, name)

        self.SetDoubleBuffered(True)
        self.CreateStatusBar()
        self.SetStatusText('wxPython %s' % wx.version())

        b = 25
        vbSizer = wx.BoxSizer(wx.VERTICAL)
        vbSizer.Add(ShapedBitmapButtonPanel8(self), 1, wx.EXPAND | wx.ALL, b)

        # self.SetSizerAndFit(vbSizer)
        self.SetSizer(vbSizer)
        self.Fit()

        # self.SetMinSize((100, 100))
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

        b = wx.Button(self, -1, 'Show ShapedBitmapButton Background GridSizer Demo', pos=(50, 50))
        b.Bind(wx.EVT_BUTTON, self.OnShowShapedBitmapButton)

    def OnShowShapedBitmapButton(self, event):
        gMainWin = ShapedBitmapButtonFrame(self)
        gMainWin.SetTitle('ShapedBitmapButton Demo')
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
