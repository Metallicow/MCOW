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


class zShapedBitmapButtonPanel0(wx.Panel):
    """Sizers Positioning of the ShapedBitmapButton with tiled seamless background bitmap."""
    def __init__(self, parent, id=wx.ID_ANY,
                 pos=wx.DefaultPosition, size=wx.DefaultSize,
                 style=wx.BORDER_SUNKEN, name='panel'):
        wx.Panel.__init__(self, parent, id, pos, size, style, name)

        bmp1 = wx.Bitmap(gImgDir + os.sep + 'shapedbutton-normal.png')
        bmp2 = wx.Bitmap(gImgDir + os.sep + 'shapedbutton-pressed.png')
        bmp3 = wx.Bitmap(gImgDir + os.sep + 'shapedbutton-hover.png')

        bmp4 = wx.Bitmap(gImgDir + os.sep + 'arrowcenterdot32.png')
        bmp5 = wx.Bitmap(gImgDir + os.sep + 'arrowcenterdot32-pressed.png')
        bmp6 = wx.Bitmap(gImgDir + os.sep + 'arrowcenterdot32-hover.png')

        btn1 = SBB.ShapedBitmapButton(self, -1, bitmap=bmp1,
                                      pressedBmp=bmp2,
                                      hoverBmp=bmp3,
                                      pos=(50, 50))
        btn1.Bind(wx.EVT_BUTTON, self.OnToggleBackground)

        btn1.MakeChildBmp()

        btn2 = SBB.ShapedBitmapButton(btn1, -1, bitmap=bmp4,
                                      pressedBmp=bmp5,
                                      hoverBmp=bmp6,
                                      pos=(50, 50))
        btn2.Bind(wx.EVT_BUTTON, self.OnClick)
        
        btn3 = SBB.ShapedBitmapButton(btn1, -1, bitmap=bmp4,
                                      pressedBmp=bmp5,
                                      hoverBmp=bmp6,
                                      pos=(10, 10))
        btn3.Bind(wx.EVT_BUTTON, self.OnClick)

    def OnToggleBackground(self, event):
        self.SetBackgroundColour(random_hex_color())
        self.Refresh()

    def OnClick(self, event):
        print('OnClick')


class ShapedBitmapButtonPanel0(wx.Panel):
    """Sizers Positioning of the ShapedBitmapButton with tiled seamless background bitmap."""
    def __init__(self, parent, id=wx.ID_ANY,
                 pos=wx.DefaultPosition, size=wx.DefaultSize,
                 style=wx.BORDER_SUNKEN, name='panel'):
        wx.Panel.__init__(self, parent, id, pos, size, style, name)

        bmp1 = wx.Bitmap(gImgDir + os.sep + 'snakey_outline128.png')
        bmp2 = wx.Bitmap(gImgDir + os.sep + 'snakey_outline_pressed128.png')
        bmp3 = wx.Bitmap(gImgDir + os.sep + 'snakey_outline_hover128.png')

        bmp4 = wx.Bitmap(gImgDir + os.sep + 'snakey_skin96.png')
        bmp5 = wx.Bitmap(gImgDir + os.sep + 'snakey_skin_pressed96.png')
        bmp6 = wx.Bitmap(gImgDir + os.sep + 'snakey_skin_hover96.png')

        # bmp4 = wx.Bitmap(gImgDir + os.sep + 'arrowcenterdot32.png')
        # bmp5 = wx.Bitmap(gImgDir + os.sep + 'arrowcenterdot32-pressed.png')
        # bmp6 = wx.Bitmap(gImgDir + os.sep + 'arrowcenterdot32-hover.png')

        btn1 = SBB.ShapedBitmapButton(self, -1, bitmap=bmp1,
                                      pressedBmp=bmp2,
                                      hoverBmp=bmp3,
                                      pos=(50, 50),
                                      style=wx.BORDER_SIMPLE)
        btn1.Bind(wx.EVT_BUTTON, self.OnToggleBackground)

        btn1.MakeChildBmp()

        btn2 = SBB.ShapedBitmapButton(btn1, -1, bitmap=bmp4,
                                      pressedBmp=bmp5,
                                      hoverBmp=bmp6,
                                      pos=(16, 16)) # Don't
        btn2.Bind(wx.EVT_BUTTON, self.OnToggleBackground)

        # btn1 = SBB.ShapedBitmapButton(self, -1, bitmap=bmp1)
        # btn1.Bind(wx.EVT_BUTTON, self.OnToggleBackground)
        self.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)


    def OnLeftUp(self, event):
        print('Panel LeftUp')
        
    def OnToggleBackground(self, event):
        self.SetBackgroundColour(random_hex_color())
        self.Refresh()


class ShapedBitmapButtonFrame(wx.Frame):
    def __init__(self, parent, id=wx.ID_ANY, title=wx.EmptyString,
                 pos=wx.DefaultPosition, size=wx.DefaultSize,
                 style=wx.DEFAULT_FRAME_STYLE, name='frame'):
        wx.Frame.__init__(self, parent, id, title, pos, size, style, name)

        # wx.Log.EnableLogging(False)

        ## self.SetDoubleBuffered(True)
        self.CreateStatusBar()
        self.SetStatusText('wxPython %s' % wx.version())

        b = 5
        vbSizer = wx.BoxSizer(wx.VERTICAL)
        vbSizer.Add(ShapedBitmapButtonPanel0(self), 1, wx.EXPAND | wx.ALL, b)

        # self.SetSizerAndFit(vbSizer)
        self.SetSizer(vbSizer)
        # self.Fit()

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

        b = wx.Button(self, -1, 'Show ShapedBitmapButton Demo', pos=(50, 50))
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
