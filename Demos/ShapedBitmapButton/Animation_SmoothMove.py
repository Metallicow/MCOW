#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
DemoName.__doc__
"""

#-Imports-----------------------------------------------------------------------

#--Python Imports.
import os
import sys

#--wxPython Imports.
# import wxversion
# wxversion.select('2.8.12.1')
## wxversion.select('2.9.4')
## wxversion.select('2.9.5-msw')
## wxversion.select('3.0.0-msw')
## wxversion.select('2.9.5.81-phoenix')
# wxversion.select('3.0.3-msw-phoenix')
import wx

try:  # Locally
    from mcow.animation import SmoothMove
    import mcow.shapedbitmapbutton as SBB
except ImportError:  # wxPython library
    from wx.lib.mcow.animation import SmoothMove
    import wx.lib.mcow.shapedbitmapbutton as SBB

gFileDir = os.path.dirname(os.path.abspath(__file__))
gImgDir = gFileDir + os.sep + 'bitmaps'
#- Demo ------------------------------------------------------------------------

__wxPyDemoPanel__ = 'TestPanel'


class TestPanel(wx.Panel):
    def __init__(self, parent, log=sys.stdout):
        self.log = log
        wx.Panel.__init__(self, parent, -1)
        self.SetDoubleBuffered(True)

        self.SetBackgroundColour(wx.WHITE)
        # self.SetBackgroundColour(wx.BLUE)
        # bgBmp = wx.Bitmap(gImgDir + os.sep + 'seamless' + os.sep + 'transparentbackground32.png', wx.BITMAP_TYPE_PNG)
        bgBmp = wx.Bitmap(gImgDir + os.sep + 'seamless' + os.sep + 'metalgriddark46x24.png', wx.BITMAP_TYPE_PNG)
        self.backgroundBitmap = SBB.MakeDisplaySizeBackgroundBitmap(bgBmp)

        #self.Refresh()
        bmp1 = wx.Bitmap(gImgDir + os.sep + 'shapedbutton-normal.png')
        bmp2 = wx.Bitmap(gImgDir + os.sep + 'shapedbutton-pressed.png')
        bmp3 = wx.Bitmap(gImgDir + os.sep + 'shapedbutton-hover.png')
        bmp4 = wx.Bitmap(gImgDir + os.sep + 'shapedbutton-disabled.png')
        fnt = wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT)
        fnt.SetWeight(wx.FONTWEIGHT_BOLD)
        fnt.SetStyle(wx.FONTSTYLE_ITALIC)
        fnt.SetPointSize(11)
        print('WillLabelTextFitInsideButton',
              SBB.ShapedBitmapButtonAdv.WillLabelTextFitInsideButton(bmp1, 'Test'*10))
        self.ctrl1 = SBB.ShapedBitmapButtonAdv(self, -1,
            bitmap=bmp1,
            pressedBmp=bmp2,
            hoverBmp=bmp3,
            disabledBmp=bmp4,
            parentBgBmp=self.backgroundBitmap,
            label='>-Arrow->',
            # label='Multi\nLine\nlabel',
            # labelRotation=20,
            # labelPosition=(5, 64),
            labelFont=fnt,
            # labelBackgroundMode=wx.SOLID,
            name='arrow'
            )

        self.ctrl1cld = SBB.ShapedBitmapButtonAdv(self.ctrl1, -1,
           bitmap=wx.Bitmap(gImgDir + os.sep + 'arrowcenterdot32.png'),
           pressedBmp=wx.Bitmap(gImgDir + os.sep + 'arrowcenterdot32-pressed.png'),
           hoverBmp=wx.Bitmap(gImgDir + os.sep + 'arrowcenterdot32-hover.png'),
           disabledBmp=wx.Bitmap(gImgDir + os.sep + 'arrowcenterdot32-disabled.png'),
           # parentBgBmp=self.backgroundBitmap
           pos=(50, 50),
           name='dot'
           )

        # bgColor = wx.CallAfter(self.GetBackgroundColour)
        # wx.CallAfter(self.ctrl.SetBackgroundColour, bgColor)
        # wx.CallAfter(self.ctrl.Refresh)
        # wx.CallAfter(self.ctrl.UpdateBackgroundColourFromParent)

        # self.ctrl2 = wx.Button(self, -1, "AnimatedMove Ctrl To Pos", (50, 50))
        # self.ctrl2 = wx.StaticBitmap(self, -1, wx.Bitmap(gImgDir + os.sep + "phoenix128.png"), (150, 150))
        self.ctrl2 = SBB.ShapedBitmapButtonAdv(self, -1,
            bitmap=wx.Bitmap(gImgDir + os.sep + "phoenix128.png"),
            #pressedBmp=bmp2,
            hoverBmp=wx.Bitmap(gImgDir + os.sep + "phoenix128-hover.png"),
            #disabledBmp=bmp4,
            parentBgBmp=self.backgroundBitmap,
            pos=(100, 75),
            name='phoenix'
            )
        self.ctrl2.SetLabelsList(
            labelsList=['wxPython %s' % wx.version(), 'rotated', 'test'],
            coords=[(0,0),(64,64),(0,100)],
            foregrounds=[wx.RED,wx.BLUE,wx.GREEN],
            backgrounds=[wx.LIGHT_GREY, wx.TransparentColour, wx.Colour(255,128,0)],
            fonts=[fnt,fnt,fnt],
            rotations=[0.0,45.0,0.0]
            )

        self.ctrl3 = SBB.ShapedBitmapButtonAdv(self, -1,
            bitmap=wx.Bitmap(gImgDir + os.sep + "bigcheck128.png"),
            pressedBmp=wx.Bitmap(gImgDir + os.sep + "bigcheck128-pressed.png"),
            hoverBmp=wx.Bitmap(gImgDir + os.sep + "bigcheck128-hover.png"),
            disabledBmp=wx.Bitmap(gImgDir + os.sep + "bigcheck128-disabled.png"),
            parentBgBmp=self.backgroundBitmap,
            pos=(100, 200),
            name='bigcheck',
            ## style=wx.BORDER
            )

        # mdc = wx.MemoryDC(wx.EmptyBitmap(100, 32))
        # mdc.Clear()
        # transBmp = mdc.GetAsBitmap(wx.Rect(0, 0, 100, 32))
        self.ctrl4 = SBB.ShapedBitmapButtonAdv(self, -1,
            # bitmap=wx.Bitmap(gImgDir + os.sep + "transparentpixel.png").ConvertToImage().Rescale(100, 32).ConvertToBitmap(),
            bitmap=wx.Bitmap(gImgDir + os.sep + "transparent16.png").ConvertToImage().Rescale(100, 32).ConvertToBitmap(),
            # pressedBmp=wx.Bitmap(gImgDir + os.sep + "bigcheck128-pressed.png"),
            hoverBmp=wx.Bitmap(gImgDir + os.sep + "menu_hover16.png").ConvertToImage().Rescale(100, 32).ConvertToBitmap(),
            # disabledBmp=wx.Bitmap(gImgDir + os.sep + "bigcheck128-disabled.png"),
            parentBgBmp=self.backgroundBitmap,
            pos=(250, 200),
            label='File',
            labelForeColour=wx.BLUE,
            name='file menu',
            ## style=wx.BORDER
            )

        self.ctrl1.Bind(wx.EVT_BUTTON, self.OnButton)
        self.ctrl2.Bind(wx.EVT_BUTTON, self.OnButton)
        self.ctrl3.Bind(wx.EVT_BUTTON, self.OnButton)
        self.ctrl1.SetDoubleBuffered(True)
        self.ctrl2.SetDoubleBuffered(True)
        self.ctrl3.SetDoubleBuffered(True)

        self.Bind(wx.EVT_LEFT_UP, self.AnimatedMoveCtrlToPos)
        self.Bind(wx.EVT_MIDDLE_UP, self.AnimatedMoveCtrlToPos)
        self.Bind(wx.EVT_RIGHT_UP, self.AnimatedMoveCtrlToPos)
        self.Bind(wx.EVT_PAINT, self.OnPaint)

        # Tests to see events passing through the alpha region in the shapedbitmapbuttons
        self_Bind = self.Bind
        # self_Bind(wx.EVT_MOTION, self.OnMotion)
        self_Bind(wx.EVT_MOUSEWHEEL, self.OnMouseWheel)
        self_Bind(wx.EVT_MIDDLE_DOWN, self.OnMiddleDown)

    def OnPaint(self, event):
        if not self:
            return
        dc = wx.BufferedPaintDC(self)
        dc.Clear()
        dc.DrawBitmap(self.backgroundBitmap, 0, 0, True)

    def OnMouseWheel(self, event):
        event.Skip()
        print('OnMouseWheel')
    def OnMotion(self, event):
        event.Skip()
        # print('OnMotion %s' % str(event.GetPosition()))
    def OnMiddleDown(self, event):
        event.Skip()
        print('OnMiddleDown')
        r1 = self.ctrl1.GetRegion()
        r2 = self.ctrl2.GetRegion()
        print('region1', r1.GetBox())
        print('region2', r2.GetBox())

        print('self.GetSizer', self.GetSizer())
        print('self.ctrl1.GetSizer', self.ctrl1.GetSizer())

        ctrl1Sibs = self.ctrl1.GetSBBSiblings()
        ctrl1cldSibs = self.ctrl1cld.GetSBBSiblings()
        print('self.ctrl1.GetSBBSiblings', ctrl1Sibs)
        print('self.ctrl1cld.GetSBBSiblings', ctrl1cldSibs)

        rect1 = self.ctrl1.GetRect()
        rect2 = self.ctrl2.GetRect()
        print('rect1', rect1)
        print('rect2', rect2)
        print('rect1 intersects rect2', rect1.Intersects(rect2))
        print('rect1 intersects rect2', rect1.Intersect(rect2))

    def OnButton(self, event):
        evtObj = event.GetEventObject()
        print('\nClicked Button %s' % evtObj.GetName())

    def AnimatedMoveCtrlToPos(self, event=None, ctrl=None, pos=None):
        moveToPos = event.GetPosition()
        # event.Skip()
        if event.GetButton() == wx.MOUSE_BTN_LEFT:
            ctrl = self.ctrl1
        elif event.GetButton() == wx.MOUSE_BTN_RIGHT:
            ctrl = self.ctrl2
        elif event.GetButton() == wx.MOUSE_BTN_MIDDLE:
            ctrl = self.ctrl3
        SmoothMove(ctrl, moveToPos)
        # event.Skip()


#- wxPython Demo ---------------------------------------------------------------


def runTest(frame, nb, log):
    win = TestPanel(nb, log)
    return win


overview = """<html><body>
<h2><center>Animation Move Ctrl Demo</center></h2>

Animate a control to a point in the Client Area...

</body></html>
"""


#- __main__ Demo ---------------------------------------------------------------


class printLog:
    def __init__(self):
        pass

    def write(self, txt):
        print('%s' % txt)

    def WriteText(self, txt):
        print('%s' % txt)


class TestFrame(wx.Frame):
    def __init__(self, parent, id=wx.ID_ANY, title=wx.EmptyString,
                 pos=wx.DefaultPosition, size=wx.DefaultSize,
                 style=wx.DEFAULT_FRAME_STYLE, name='frame'):
        wx.Frame.__init__(self, parent, id, title, pos, size, style, name)

        log = printLog()

        wxVER = 'wxPython %s' % wx.version()
        pyVER = 'python %d.%d.%d.%s' % sys.version_info[0:4]
        versionInfos = '%s %s' % (wxVER, pyVER)
        self.CreateStatusBar().SetStatusText(versionInfos)

        panel = TestPanel(self, log)
        self.Bind(wx.EVT_CLOSE, self.OnDestroy)

        try:
            iconLoc = wx.IconLocation(sys.executable)
            icon = wx.IconFromLocation(iconLoc)
            self.SetIcon(icon)
        except Exception as exc:
            pass

    def OnDestroy(self, event):
        self.Destroy()


class TestApp(wx.App):
    def OnInit(self):
        gMainWin = TestFrame(None)
        gMainWin.SetTitle('SmoothMove Demo')
        gMainWin.Show()
        gMainWin.Centre()

        return True


#- __main__ --------------------------------------------------------------------



if __name__ == '__main__':
    import sys
    print('Python %s.%s.%s %s' % sys.version_info[0:4])
    print('wxPython %s' % wx.version())
    gApp = TestApp(redirect=False,
                   filename=None,
                   useBestVisual=False,
                   clearSigInt=True)
    gApp.MainLoop()
