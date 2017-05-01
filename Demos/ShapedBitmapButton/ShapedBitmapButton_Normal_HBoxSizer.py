#!/usr/bin/env python
# -*- coding: utf-8 -*-

#-Imports-----------------------------------------------------------------------

#--Python Imports.
import os
import sys
import random

#--wxPython Imports.
# import wxversion
# wxversion.select('2.8')
# wxversion.select('3.0.3-msw-phoenix')
import wx

try:  # Locally
    import mcow.shapedbitmapbutton as SBB
except ImportError:  # wxPython library
    import wx.lib.mcow.shapedbitmapbutton as SBB

__wxPyDemoPanel__ = 'TestPanel'
#-Globals-----------------------------------------------------------------------
gFileDir = os.path.dirname(os.path.abspath(__file__))
gImgDir = gFileDir + os.sep + 'bitmaps'
gShuffle = random.shuffle
HEX = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
       'a', 'b', 'c', 'd', 'e', 'f']
DIRECTIONS = [wx.NORTH, wx.SOUTH, wx.EAST, wx.WEST]


def random_hex_color():
    gShuffle(HEX) # Order is random now
    ## print(HEX)
    randomcolor = ''
    for item in range(0,6):
        gShuffle(HEX) # Twice for doubles and good luck :)
        ## print(HEX[item])
        randomcolor = randomcolor + u'%s'%(HEX[item])
    ## print(randomcolor)
    return u'#%s' %(randomcolor)


class ShapedBitmapButtonPanel3(wx.Panel):
    """
    Sizers Positioning of the ShapedBitmapButton with panel bgColour.
    """
    def __init__(self, parent, id=wx.ID_ANY,
                 pos=wx.DefaultPosition, size=wx.DefaultSize,
                 style=wx.BORDER_SUNKEN, name='panel'):
        wx.Panel.__init__(self, parent, id, pos, size, style, name)

        self.SetBackgroundColour(wx.GREEN)
        button1 = SBB.ShapedBitmapButton(self, -1,
            bitmap=wx.Bitmap(gImgDir + os.sep + 'shapedbutton-normal.png'),
            pressedBmp=wx.Bitmap(gImgDir + os.sep + 'shapedbutton-pressed.png'),
            hoverBmp=None,
            disabledBmp=wx.Bitmap(gImgDir + os.sep + 'shapedbutton-disabled.png'),
            style=wx.NO_BORDER | wx.WANTS_CHARS)

        button2 = SBB.ShapedBitmapButton(self, -1,
            bitmap=wx.Bitmap(gImgDir + os.sep + 'shapedbutton-normal.png'),
            pressedBmp=wx.Bitmap(gImgDir + os.sep + 'shapedbutton-pressed.png'),
            hoverBmp=wx.Bitmap(gImgDir + os.sep + 'shapedbutton-hover.png'),
            disabledBmp=wx.Bitmap(gImgDir + os.sep + 'shapedbutton-disabled.png'),
            label='Hello World!', labelPosition=(5, 67), labelRotation=24.0,
            labelFont=wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD),
            style=wx.BORDER_SIMPLE | wx.WANTS_CHARS)

        button3 = SBB.ShapedBitmapButton(self, -1,
            bitmap=wx.Bitmap(gImgDir + os.sep + 'shapedbutton-normal.png'),
            pressedBmp=wx.Bitmap(gImgDir + os.sep + 'shapedbutton-pressed.png'),
            hoverBmp=None,
            disabledBmp=wx.Bitmap(gImgDir + os.sep + 'shapedbutton-disabled.png'),
            style=wx.BORDER_NONE)
        button3.Disable()

        button4 = SBB.ShapedBitmapButton(self, -1,
            bitmap=wx.Bitmap(gImgDir + os.sep + 'shapedbutton-normal.png'),
            pressedBmp=wx.Bitmap(gImgDir + os.sep + 'shapedbutton-pressed.png'),
            hoverBmp=None,
            disabledBmp=None)
        button4.Disable()

        hbSizer = wx.BoxSizer(wx.HORIZONTAL)
        for btn in self.GetChildren():
            btn.Bind(wx.EVT_BUTTON, self.OnRandomBackgroundColour)
            hbSizer.Add(btn, 1, wx.EXPAND | wx.ALL, 5)
        self.SetSizer(hbSizer)

    def OnRandomBackgroundColour(self, event):
        """Randomize the backgroundBitmap."""
        self.SetBackgroundColour(random_hex_color())
        self.Refresh()


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

        vbSizer.Add(ShapedBitmapButtonPanel3(self), 0, wx.EXPAND | wx.TOP | wx.LEFT | wx.RIGHT, b)

        # self.SetSizerAndFit(vbSizer)
        self.SetSizer(vbSizer)
        self.Fit()

        self.Bind(wx.EVT_CLOSE, self.OnDestroy)

    def OnDestroy(self, event):
        self.Destroy()


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

        b = wx.Button(self, -1, 'Show ShapedBitmapButton Normal Sizers Demo', pos=(50, 50))
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
    import sys
    print(wx.version())
    gApp = ShapedBitmapButtonApp(redirect=False,
            filename=None,
            useBestVisual=False,
            clearSigInt=True)

    gApp.MainLoop()
