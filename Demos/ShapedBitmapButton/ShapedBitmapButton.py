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
# wxversion.select('3.0-msw')
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


class ShapedBitmapButtonPanel0(wx.Panel):
    """Sizers Positioning of the ShapedBitmapButton with tiled seamless background bitmap."""
    def __init__(self, parent, id=wx.ID_ANY,
                 pos=wx.DefaultPosition, size=wx.DefaultSize,
                 style=wx.BORDER_SUNKEN, name='panel'):
        wx.Panel.__init__(self, parent, id, pos, size, style, name)

        ## self.SetDoubleBuffered(True) # Possibly Overkill

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
        flags = wx.EXPAND | wx.ALL
        try:
            hbSizer = wx.WrapSizer(wx.HORIZONTAL)
        except Exception:
            hbSizer = wx.BoxSizer(wx.HORIZONTAL)
        for i in range(25):
            btn = ShapedBitmapButton(self, -1,
                bitmap=bmp1,
                pressedBmp=bmp2,
                hoverBmp=bmp3,
                disabledBmp=bmp4,
                parentBgBmp=self.backgroundBitmap)
            btn.Bind(wx.EVT_BUTTON, self.OnToggleBackground)
            hbSizer.Add(btn, p, flags, b)

        self.SetSizer(hbSizer)

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
            for child in self.GetChildren() if isinstance(child, ShapedBitmapButton)]
        self.Refresh()

    def OnPaint(self, event):
        dc = wx.BufferedPaintDC(self)
        dc.Clear()
        dc.DrawBitmap(self.backgroundBitmap, 0, 0, True)


class ShapedBitmapButtonPanel1(wx.Panel):
    """Sizers Positioning of the ShapedBitmapButton with tiled seamless background bitmap."""
    def __init__(self, parent, id=wx.ID_ANY,
                 pos=wx.DefaultPosition, size=wx.DefaultSize,
                 style=wx.BORDER_SUNKEN, name='panel'):
        wx.Panel.__init__(self, parent, id, pos, size, style, name)

        ## self.SetDoubleBuffered(True) # Possibly Overkill

        # Drawing performance is faster with a tilable bitmap about
        # the same size as what you are going to tile(In this case, the panel).
        # It also helps to optimize the images(reduce size/retain image quality)
        # with a application such as FileOptimizer
        bgBmp = wx.Bitmap(gImgDir + os.sep + 'seamless' + os.sep + 'transparentbackground32.png', wx.BITMAP_TYPE_PNG)
        self.backgroundBitmap = SBB.MakeDisplaySizeBackgroundBitmap(bgBmp)
        # Slight flicker is less noticable at the edge when resizing if you use
        # a colour used most/close in the bitmap.
        self.SetBackgroundColour(wx.WHITE)

        button1 = ShapedBitmapButton(self, -1,
            bitmap=wx.Bitmap(gImgDir + os.sep + 'shapedbutton-normal.png'),
            pressedBmp=wx.Bitmap(gImgDir + os.sep + 'shapedbutton-pressed.png'),
            hoverBmp=None,
            disabledBmp=wx.Bitmap(gImgDir + os.sep + 'shapedbutton-disabled.png'),
            parentBgBmp=self.backgroundBitmap,
            style=wx.NO_BORDER | wx.WANTS_CHARS)
        button1.SetToolTip(wx.ToolTip('This is a ShapedBitmapButton.\n'
                                      'The hoverBmp has NOT been set for this one.'))

        button2 = ShapedBitmapButton(self, -1,
            bitmap=wx.Bitmap(gImgDir + os.sep + 'shapedbutton-normal.png'),
            pressedBmp=wx.Bitmap(gImgDir + os.sep + 'shapedbutton-pressed.png'),
            hoverBmp=wx.Bitmap(gImgDir + os.sep + 'shapedbutton-hover.png'),
            disabledBmp=wx.Bitmap(gImgDir + os.sep + 'shapedbutton-disabled.png'),
            parentBgBmp=self.backgroundBitmap,
            style=wx.NO_BORDER | wx.WANTS_CHARS)
        button2.SetToolTip(wx.ToolTip('This is a ShapedBitmapButton.\n'
                                      'The hoverBmp HAS been set on this one.'))

        button3 = ShapedBitmapButton(self, -1,
            bitmap=wx.Bitmap(gImgDir + os.sep + 'shapedbutton-normal.png'),
            pressedBmp=wx.Bitmap(gImgDir + os.sep + 'shapedbutton-pressed.png'),
            hoverBmp=None,
            disabledBmp=wx.Bitmap(gImgDir + os.sep + 'shapedbutton-disabled.png'),
            parentBgBmp=self.backgroundBitmap,
            )
        button3.Disable()

        button4 = ShapedBitmapButton(self, -1,
            bitmap=wx.Bitmap(gImgDir + os.sep + 'shapedbutton-normal.png'),
            pressedBmp=wx.Bitmap(gImgDir + os.sep + 'shapedbutton-pressed.png'),
            hoverBmp=None,
            disabledBmp=None,
            parentBgBmp=self.backgroundBitmap,
            )
        button4.Disable()

        for btn in self.GetChildren():
            btn.Bind(wx.EVT_BUTTON, self.OnToggleBackground)
        self.Bind(wx.EVT_PAINT, self.OnPaint)

        hbSizer = wx.BoxSizer(wx.HORIZONTAL)
        p = 1
        b = 5
        ## flags = wx.ALIGN_CENTRE | wx.ALL
        flags = wx.EXPAND | wx.ALL
        hbSizer.Add(button1, p, flags, b)
        hbSizer.Add(button2, p, flags, b)
        hbSizer.Add(button3, p, flags, b)
        hbSizer.Add(button4, p, flags, b)
        self.SetSizer(hbSizer)

    ## Additionally reduce OnSize bg bmp flicker of the buttons while resizing. ####
        self.Bind(wx.EVT_SIZE, self.OnSize)                                     #
        #self.SetDoubleBuffered(True)                                            #
                                                                                #
    def OnSize(self, event):                                                    #                                                     #
        #self.Freeze()
        #self.Refresh()
        self.Layout()                                                           #
        #self.Thaw()
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
            for child in self.GetChildren() if isinstance(child, ShapedBitmapButton)]
        self.Refresh()

    def OnPaint(self, event):
        dc = wx.BufferedPaintDC(self)
        dc.Clear()
        dc.DrawBitmap(self.backgroundBitmap, 0, 0, True)


class ShapedBitmapButtonPanel2(wx.Panel):
    """Absolute Positioning of the ShapedBitmapButton with gradient background bitmap."""
    def __init__(self, parent, id=wx.ID_ANY,
                 pos=wx.DefaultPosition, size=wx.DefaultSize,
                 style=wx.BORDER_SUNKEN, name='panel'):
        wx.Panel.__init__(self, parent, id, pos, size, style, name)

        ## self.SetDoubleBuffered(True) # Possibly Overkill
        self.gradientColor1 = '#FF8000'
        self.gradientColor2 = '#000000'
        self.gradientDirection = wx.NORTH

        self.backgroundBitmap = self.MakeBackgroundBitmap()
        wx.CallAfter(self.MakeBackgroundBitmap)
        self.Bind(wx.EVT_PAINT, self.OnPaint)

        button1 = ShapedBitmapButton(self, -1,
            bitmap=wx.Bitmap(gImgDir + os.sep + 'arrowcenterdot32.png'),
            pressedBmp=wx.Bitmap(gImgDir + os.sep + 'arrowcenterdot32-pressed.png'),
            hoverBmp=wx.Bitmap(gImgDir + os.sep + 'arrowcenterdot32-hover.png'),
            disabledBmp=wx.Bitmap(gImgDir + os.sep + 'arrowcenterdot32-disabled.png'),
            pos=(15, 15), style=wx.NO_BORDER | wx.WANTS_CHARS)
        button1.SetToolTip(wx.ToolTip('This is a ShapedBitmapButton.'))

        button2 = ShapedBitmapButton(self, -1,
            bitmap=wx.Bitmap(gImgDir + os.sep + 'bigcheck128.png'),
            pressedBmp=wx.Bitmap(gImgDir + os.sep + 'bigcheck128-pressed.png'),
            hoverBmp=wx.Bitmap(gImgDir + os.sep + 'bigcheck128-hover.png'),
            disabledBmp=wx.Bitmap(gImgDir + os.sep + 'bigcheck128-disabled.png'),
            pos=(60, 15), style=wx.NO_BORDER | wx.WANTS_CHARS)
        button2.SetToolTip(wx.ToolTip('This is a ShapedBitmapButton.'))

        button3 = ShapedBitmapButton(self, -1,
            bitmap=wx.Bitmap(gImgDir + os.sep + 'arrowcenterdot32.png'),
            pressedBmp=wx.Bitmap(gImgDir + os.sep + 'arrowcenterdot32-pressed.png'),
            hoverBmp=None,
            disabledBmp=wx.Bitmap(gImgDir + os.sep + 'arrowcenterdot32-disabled.png'),
            pos=(256, 64))
        ## button3.Disable()

        button4 = ShapedBitmapButton(self, -1,
            bitmap=wx.Bitmap(gImgDir + os.sep + 'arrowcenterdot32.png'),
            pressedBmp=wx.Bitmap(gImgDir + os.sep + 'arrowcenterdot32-pressed.png'),
            hoverBmp=None,
            disabledBmp=None,
            pos=(220, 0))
        ## button4.Disable()

        button1.Bind(wx.EVT_BUTTON, self.OnRandomGradient)
        button2.Bind(wx.EVT_BUTTON, self.OnRandomGradient)
        button3.Bind(wx.EVT_BUTTON, self.OnRandomGradient)
        button4.Bind(wx.EVT_BUTTON, self.OnRandomGradient)


    def OnRandomGradient(self, event):
        """Toggle the backgroundBitmap"""
        print('self.GetClientSize()', self.GetClientSize())
        print('self.GetSize()', self.GetSize())
        self.gradientColor1 = random_hex_color()
        self.gradientColor2 = random_hex_color()
        random.shuffle(DIRECTIONS)
        self.gradientDirection = DIRECTIONS[0]
        self.Refresh()

    def MakeBackgroundBitmap(self, set=False):
        width, height = self.GetClientSize()
        # width, height = self.GetSize()
        # width, height = wx.GetDisplaySize()

        mdc = wx.MemoryDC(wx.EmptyBitmap(width, height))

        mdc.GradientFillLinear(rect=(0, 0, width, height),
                              initialColour=self.gradientColor1,
                              destColour=self.gradientColor2,
                              nDirection=self.gradientDirection)

        if set:
            self.backgroundBitmap = mdc.GetAsBitmap(wx.Rect(0, 0, width, height))
        else:
            return mdc.GetAsBitmap(wx.Rect(0, 0, width, height))
        # try:
            # return mdc.GetAsBitmap(wx.Rect(0, 0, width, height))
        # except wx._core.PyAssertionError:
            # print('EXCEPTION', width, height)
            # return wx.EmptyBitmap(64, 64)

    """
    @ Important function: GetBackgroundBitmap
    Add this def to your code if you desire a seamless gradient background
    look with the ShapedBitmapButton.
    """
    def GetBackgroundBitmap(self):
        # return self.backgroundBitmap

        # width, height = self.GetClientSize()
        # width, height = self.GetSize()
        width, height = self.Size[0], self.Size[1]

        mdc = wx.MemoryDC(wx.EmptyBitmap(width, height))

        mdc.GradientFillLinear(rect=(0, 0, width, height),
                              initialColour=self.gradientColor1,
                              destColour=self.gradientColor2,
                              nDirection=self.gradientDirection)

        return mdc.GetAsBitmap(wx.Rect(0, 0, width, height))

    def OnPaint(self, event):
        pdc = wx.BufferedPaintDC(self)
        pdc.Clear()
        pdc.DrawBitmap(self.GetBackgroundBitmap(), 0, 0, True)


class ShapedBitmapButtonPanel3(wx.Panel):
    """
    Sizers Positioning of the ShapedBitmapButton with panel bgColour.
    """
    def __init__(self, parent, id=wx.ID_ANY,
                 pos=wx.DefaultPosition, size=wx.DefaultSize,
                 style=wx.BORDER_SUNKEN, name='panel'):
        wx.Panel.__init__(self, parent, id, pos, size, style, name)

        ## self.SetDoubleBuffered(True) # Possibly Overkill

        self.SetBackgroundColour(wx.GREEN)
        button1 = ShapedBitmapButton(self, -1,
            bitmap=wx.Bitmap(gImgDir + os.sep + 'shapedbutton-normal.png'),
            pressedBmp=wx.Bitmap(gImgDir + os.sep + 'shapedbutton-pressed.png'),
            hoverBmp=None,
            disabledBmp=wx.Bitmap(gImgDir + os.sep + 'shapedbutton-disabled.png'),
            style=wx.NO_BORDER | wx.WANTS_CHARS)

        button2 = ShapedBitmapButton(self, -1,
            bitmap=wx.Bitmap(gImgDir + os.sep + 'shapedbutton-normal.png'),
            pressedBmp=wx.Bitmap(gImgDir + os.sep + 'shapedbutton-pressed.png'),
            hoverBmp=wx.Bitmap(gImgDir + os.sep + 'shapedbutton-hover.png'),
            disabledBmp=wx.Bitmap(gImgDir + os.sep + 'shapedbutton-disabled.png'),
            label='Hello World!', labelPosition=(5, 67), labelRotation=24.0,
            labelFont=wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD),
            style=wx.BORDER_SIMPLE | wx.WANTS_CHARS)

        button3 = ShapedBitmapButton(self, -1,
            bitmap=wx.Bitmap(gImgDir + os.sep + 'shapedbutton-normal.png'),
            pressedBmp=wx.Bitmap(gImgDir + os.sep + 'shapedbutton-pressed.png'),
            hoverBmp=None,
            disabledBmp=wx.Bitmap(gImgDir + os.sep + 'shapedbutton-disabled.png'),
            style=wx.BORDER_NONE)
        button3.Disable()

        button4 = ShapedBitmapButton(self, -1,
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
        """Toggle the backgroundBitmap."""
        self.SetBackgroundColour(random_hex_color())
        self.Refresh()


class ShapedBitmapButtonPanel4(wx.Panel):
    """Absolute Positioning of the ShapedBitmapButton"""
    def __init__(self, parent, id=wx.ID_ANY,
                 pos=wx.DefaultPosition, size=(512, 160),
                 style=wx.BORDER_SUNKEN, name='panel'):
        wx.Panel.__init__(self, parent, id, pos, size, style, name)

        self.SetDoubleBuffered(True) # Possibly Overkill

        sBmp = wx.Bitmap(gImgDir + os.sep + 'bigx128.png')
        sz = self.GetSize()
        button1 = ShapedBitmapButton(self, -1,
            bitmap=sBmp,
            pressedBmp=wx.Bitmap(gImgDir + os.sep + 'bigx128-pressed.png'),
            hoverBmp=wx.Bitmap(gImgDir + os.sep + 'bigx128-hover.png'),
            disabledBmp=wx.Bitmap(gImgDir + os.sep + 'bigx128-disabled.png'),
            pos=(sz[0] // 3 , sz[1] // 2 - sBmp.GetHeight() // 2), size=(128, 128))
        button1.SetToolTip(wx.ToolTip('%s' % self.__doc__))

        button2 = ShapedBitmapButton(self, -1,
            bitmap=wx.Bitmap(gImgDir + os.sep + 'arrowcenterdot32.png'),
            pressedBmp=wx.Bitmap(gImgDir + os.sep + 'arrowcenterdot32-pressed.png'),
            hoverBmp=wx.Bitmap(gImgDir + os.sep + 'arrowcenterdot32-hover.png'),
            disabledBmp=wx.Bitmap(gImgDir + os.sep + 'arrowcenterdot32-disabled.png'),
            pos=(45, 25), style=wx.NO_BORDER | wx.WANTS_CHARS)

        button1.Bind(wx.EVT_BUTTON, self.OnButton)
        button2.Bind(wx.EVT_BUTTON, self.OnButton)

    def OnButton(self, event):
        print('buttonId %s was clicked.' % event.GetId())


class ShapedBitmapButtonFrame(wx.Frame):
    def __init__(self, parent, id=wx.ID_ANY, title=wx.EmptyString,
                 pos=wx.DefaultPosition, size=wx.DefaultSize,
                 style=wx.DEFAULT_FRAME_STYLE, name='frame'):
        wx.Frame.__init__(self, parent, id, title, pos, size, style, name)

        self.SetDoubleBuffered(True) # Possibly Overkill
        self.CreateStatusBar()
        self.SetStatusText('wxPython %s' % wx.version())

        b = 5
        vbSizer = wx.BoxSizer(wx.VERTICAL)
        vbSizer.Add(ShapedBitmapButtonPanel0(self), 0, wx.EXPAND | wx.TOP | wx.LEFT | wx.RIGHT, b)
        vbSizer.Add(ShapedBitmapButtonPanel1(self), 0, wx.EXPAND | wx.TOP | wx.LEFT | wx.RIGHT, b)
        # vbSizer.Add(ShapedBitmapButtonPanel2(self), 0, wx.ALIGN_CENTRE | wx.TOP | wx.LEFT | wx.RIGHT, b)
        vbSizer.Add(ShapedBitmapButtonPanel3(self), 0, wx.EXPAND | wx.TOP | wx.LEFT | wx.RIGHT, b)
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

        b = wx.Button(self, -1, 'Show ShapedBitmapButton Full Demo', pos=(50, 50))
        b.Bind(wx.EVT_BUTTON, self.OnShowShapedBitmapButton)

    def OnShowShapedBitmapButton(self, event):
        gMainWin = ShapedBitmapButtonFrame(self)
        gMainWin.SetTitle('ShapedBitmapButton Full Demo')
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
    print('Python %s.%s.%s %s' % sys.version_info[0:4])
    print('wxPython %s' % wx.version())
    gApp = ShapedBitmapButtonApp(redirect=False,
                                 filename=None,
                                 useBestVisual=False,
                                 clearSigInt=True)
    gApp.MainLoop()
