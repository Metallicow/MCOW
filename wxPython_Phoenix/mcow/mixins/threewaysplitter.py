#!/usr/bin/env python

#----------------------------------------------------------------------------
# Name:        wx.lib.mcow.mixins.threewaysplitter
# Purpose:     Helpful mix-in classes for wx.lib.mcow.ThreeWaySplitter
#
# Author:      Edward Greig
#
# Created:     3-Feb-2014
# Copyright:   (c) Edward Greig 2014
# Licence:     wxWindows license
#----------------------------------------------------------------------------


import wx
from wx.lib.gestures import MouseGestures


class AnimMoveMouseGestureMixin:
    """SourceCoder Library: AnimMoveMouseGestureMixin
    Mixin class that adds AnimatedMove MouseGestures to :class:`ThreeWaySplitter`'s
    windows
    based/derived classes that inherited it.


    Basic Example Usage Snippet:
        import wx
        import wx.lib.mcow.threewaysplitter as TWS
        from wx.lib.mcow.mixins.threewaysplitter import AnimMoveMouseGestureMixin


        class SampleGradientPanel(wx.Panel, AnimMoveMouseGestureMixin):
            def __init__(self, parent, gradColours):
                wx.Panel.__init__(self, parent)
                self.gradColours = gradColours
                self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)
                self.Bind(wx.EVT_PAINT, self.OnPaint)
                self.Bind(wx.EVT_SIZE, self.OnSize)
                AnimMoveMouseGestureMixin.__init__(self)

            def OnEraseBackground(self, event):
                pass

            def OnSize(self, event):
                self.Refresh()

            def OnPaint(self, event):
                dc = wx.PaintDC(self) # More buffering will slow down the AnimationMoves.
                dc.GradientFillLinear(self.GetClientRect(),
                                      self.gradColours[0], self.gradColours[1])


        class AnimMoveMouseGestureFrame(wx.Frame):
            def __init__(self, parent, id=wx.ID_ANY, title=wx.EmptyString,
                         pos=wx.DefaultPosition, size=wx.DefaultSize,
                         style=wx.DEFAULT_FRAME_STYLE, name='frame'):
                wx.Frame.__init__(self, parent, id, title, pos, size, style, name)

                self.SetDoubleBuffered(True) # Reduce gradient flicker on size.

                splitter = TWS.ThreeWaySplitter(self, agwStyle=wx.SP_LIVE_UPDATE,
                                                loneSide=wx.TOP, minSplitterSize=(50, 50))

                for ii, color in enumerate((wx.RED, '#FFFF00', wx.BLUE)):
                    panel = SampleGradientPanel(splitter, (color, wx.WHITE))
                    splitter.AppendWindow(panel)

                self.Bind(wx.EVT_CLOSE, self.OnDestroy)

            def OnDestroy(self, event):
                self.Destroy()


        class AnimMoveMouseGestureMixinApp(wx.App):
            def OnInit(self):
                gMainWin = AnimMoveMouseGestureFrame(None, size=(350, 350))
                gMainWin.SetTitle('AnimMoveMouseGestureMixin Test')
                self.SetTopWindow(gMainWin)
                gMainWin.Show()
                return True


        gApp = AnimMoveMouseGestureMixinApp(redirect=False,
                filename=None,
                useBestVisual=False,
                clearSigInt=True)

        gApp.MainLoop()

    """
    def __init__(self, gestureMouseBtn=wx.MOUSE_BTN_RIGHT,
                 gesturesVisible=True,
                 gesturePenColor=wx.Colour(255, 156, 0),
                 gesturePenWidth=5):
        """Initialize the AnimMoveMouseGestureMixin mixin"""

        self.tws = self.GetParent()
        ## print(self.tws.__class__.__name__)
        if not self.tws.__class__.__name__ == 'ThreeWaySplitter':
            raise Exception('AnimMoveMouseGestureMixin parent must be ThreeWaySplitter')

        self._gestureMouseBtn = gestureMouseBtn
        self._gesturesVisible = gesturesVisible
        self._gesturePenColor = gesturePenColor
        self._gesturePenWidth = gesturePenWidth

        self._mouseGesture = MouseGestures(self, Auto=True, MouseButton=gestureMouseBtn)
        self._mouseGesture.AddGesture('L', self.AnimLeft, 'You moved left')
        self._mouseGesture.AddGesture('U', self.AnimTop, 'You moved up')
        self._mouseGesture.AddGesture('R', self.AnimRight, 'You moved right')
        self._mouseGesture.AddGesture('D', self.AnimBottom, 'You moved down')
        # the diag gestures
        self._mouseGesture.AddGesture('1', self.AnimBottomLeft, 'You moved left/down  diag1')
        self._mouseGesture.AddGesture('3', self.AnimBottomRight, 'You moved right/down diag3')
        self._mouseGesture.AddGesture('7', self.AnimTopLeft, 'You moved left/up    diag7')
        self._mouseGesture.AddGesture('9', self.AnimTopRight, 'You moved right/up   diag9')
        # self._mouseGesture.AddGesture('' , self.OnMMouseGestureMenuNone, 'Reg Context Menu')
        self._mouseGesture.SetGesturesVisible(gesturesVisible)
        self._mouseGesture.SetGesturePen(gesturePenColor, gesturePenWidth)

    def AnimLeft(self, event):
        if self.tws.GetExpanded() == -1:
            self.tws.AnimatedMove(wx.LEFT)
            # self.tws.AnimatedMove(wx.WEST)

    def AnimTop(self, event):
        if self.tws.GetExpanded() == -1:
            self.tws.AnimatedMove(wx.TOP)
            # self.tws.AnimatedMove(wx.NORTH)

    def AnimRight(self, event):
        if self.tws.GetExpanded() == -1:
            self.tws.AnimatedMove(wx.RIGHT)
            # self.tws.AnimatedMove(wx.EAST)

    def AnimBottom(self, event):
        if self.tws.GetExpanded() == -1:
            self.tws.AnimatedMove(wx.BOTTOM)
            # self.tws.AnimatedMove(wx.SOUTH)

    def AnimTopLeft(self, event):
        if self.tws.GetExpanded() == -1:
            self.tws.AnimatedMove(wx.TOP | wx.LEFT)
            # self.tws.AnimatedMove(wx.NORTH | wx.WEST)

    def AnimTopRight(self, event):
        if self.tws.GetExpanded() == -1:
            self.tws.AnimatedMove(wx.TOP | wx.RIGHT)
            # self.tws.AnimatedMove(wx.NORTH | wx.EAST)

    def AnimBottomLeft(self, event):
        if self.tws.GetExpanded() == -1:
            self.tws.AnimatedMove(wx.BOTTOM | wx.LEFT)
            # self.tws.AnimatedMove(wx.SOUTH | wx.WEST)

    def AnimBottomRight(self, event):
        if self.tws.GetExpanded() == -1:
            self.tws.AnimatedMove(wx.BOTTOM | wx.RIGHT)
            # self.tws.AnimatedMove(wx.SOUTH | wx.EAST)


if __name__ == '__main__':
    # Test app.
    from wx.lib.gestures import MouseGestures
    import wx.lib.mcow.threewaysplitter as TWS

    class SampleGradientPanel(wx.Panel, AnimMoveMouseGestureMixin):
        def __init__(self, parent, gradColours):
            wx.Panel.__init__(self, parent)
            self.gradColours = gradColours
            self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)
            self.Bind(wx.EVT_PAINT, self.OnPaint)
            self.Bind(wx.EVT_SIZE, self.OnSize)
            AnimMoveMouseGestureMixin.__init__(self)

        def OnEraseBackground(self, event):
            pass

        def OnSize(self, event):
            self.Refresh()

        def OnPaint(self, event):
            dc = wx.PaintDC(self) # More buffering will slow down the AnimationMoves.
            dc.GradientFillLinear(self.GetClientRect(),
                                  self.gradColours[0], self.gradColours[1])


    class AnimMoveMouseGestureFrame(wx.Frame):
        def __init__(self, parent, id=wx.ID_ANY, title=wx.EmptyString,
                     pos=wx.DefaultPosition, size=wx.DefaultSize,
                     style=wx.DEFAULT_FRAME_STYLE, name='frame'):
            wx.Frame.__init__(self, parent, id, title, pos, size, style, name)

            self.SetDoubleBuffered(True) # Reduce gradient flicker on size.

            splitter = TWS.ThreeWaySplitter(self, agwStyle=wx.SP_LIVE_UPDATE,
                                            loneSide=wx.TOP, minSplitterSize=(50, 50))

            for ii, color in enumerate((wx.RED, '#FFFF00', wx.BLUE)):
                panel = SampleGradientPanel(splitter, (color, wx.WHITE))
                splitter.AppendWindow(panel)

            self.Bind(wx.EVT_CLOSE, self.OnDestroy)
            
            self.CreateStatusBar().SetStatusText('wxPython %s' % wx.version())

        def OnDestroy(self, event):
            self.Destroy()


    class AnimMoveMouseGestureMixinApp(wx.App):
        def OnInit(self):
            gMainWin = AnimMoveMouseGestureFrame(None, size=(350, 350))
            gMainWin.SetTitle('AnimMoveMouseGestureMixin Test')
            self.SetTopWindow(gMainWin)
            gMainWin.Show()
            return True


    gApp = AnimMoveMouseGestureMixinApp(redirect=False,
            filename=None,
            useBestVisual=False,
            clearSigInt=True)

    gApp.MainLoop()
