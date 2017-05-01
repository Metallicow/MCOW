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


class ShapedBitmapButtonPanel4(wx.Panel):
    """Absolute Positioning of the ShapedBitmapButton"""
    def __init__(self, parent, id=wx.ID_ANY,
                 pos=wx.DefaultPosition, size=(512, 160),
                 style=wx.BORDER_SUNKEN, name='panel'):
        wx.Panel.__init__(self, parent, id, pos, size, style, name)

        sBmp = wx.Bitmap(gImgDir + os.sep + 'bigx128.png')
        sz = self.GetSize()
        button1 = SBB.ShapedBitmapButton(self, -1,
            bitmap=sBmp,
            pressedBmp=wx.Bitmap(gImgDir + os.sep + 'bigx128-pressed.png'),
            hoverBmp=wx.Bitmap(gImgDir + os.sep + 'bigx128-hover.png'),
            disabledBmp=wx.Bitmap(gImgDir + os.sep + 'bigx128-disabled.png'),
            pos=(sz[0] // 3 , sz[1] // 2 - sBmp.GetHeight() // 2), size=(128, 128))
        button1.SetToolTip(wx.ToolTip('%s' % self.__doc__))

        button2 = SBB.ShapedBitmapButton(self, -1,
            bitmap=wx.Bitmap(gImgDir + os.sep + 'arrowcenterdot32.png'),
            pressedBmp=wx.Bitmap(gImgDir + os.sep + 'arrowcenterdot32-pressed.png'),
            hoverBmp=wx.Bitmap(gImgDir + os.sep + 'arrowcenterdot32-hover.png'),
            disabledBmp=wx.Bitmap(gImgDir + os.sep + 'arrowcenterdot32-disabled.png'),
            pos=(45, 25), style=wx.NO_BORDER | wx.WANTS_CHARS)

        button1.Bind(wx.EVT_BUTTON, self.OnButton)
        button2.Bind(wx.EVT_BUTTON, self.OnButton)
        # self.Bind(wx.EVT_CONTEXT_MENU, self.OnRightUp)
        self.Bind(wx.EVT_RIGHT_UP, self.OnRightUp)

    def OnRightUp(self, event):
        m = wx.Menu()
        m.Append(-1, 'PopupMenu')
        self.PopupMenu(m)
        m.Destroy()

    def OnButton(self, event):
        print('buttonId %s was clicked.' % event.GetId())


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

        vbSizer.Add(ShapedBitmapButtonPanel4(self), 0, wx.ALIGN_CENTRE | wx.ALL, b)

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

        b = wx.Button(self, -1, 'Show ShapedBitmapButton Normal Absolute Positioning Demo', pos=(50, 50))
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
