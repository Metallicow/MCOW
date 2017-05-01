#!/usr/bin/env python

#----------------------------------------------------------------------------
# Name:        wx.lib.mcow.mixins.toplevelwindow
# Purpose:     Helpful mix-in classes for wx.TopLevelWindow
#
# Author:      Edward Greig
#
# Created:     01-Jan-2014
# Copyright:   (c) Edward Greig 2014
# Licence:     wxWindows license
#----------------------------------------------------------------------------


import wx


#----------------------------------------------------------------------------


class TempTransparencyMoveMixin:
    """SourceCoder Library: TransparentMoveMixin
    Mixin class that handles changing of transparency of a
    TopLevelWindow by when moving it.
    WindowsXP and possibly other Operating Systems don't have this
    feature built-in by default.

    """
    def __init__(self, transparency=200):
        """Initialize the transparent move mixin
        :param `transparency`: int 1-255

        """
        # Attributes
        self._transparency = transparency

        self.Bind(wx.EVT_MOVE_START, self.OnMoveStart_TempTransparency)
        self.Bind(wx.EVT_MOVE_END, self.OnMoveEnd_TempTransparency)

    def OnMoveStart_TempTransparency(self, event):
        """
        Handles the ``wx.EVT_MOVE_START`` event.
        """
        evtObj = event.GetEventObject()
        if not evtObj.HasTransparentBackground():
            evtObj.SetTransparent(self._transparency)

    def OnMoveEnd_TempTransparency(self, event):
        """
        Handles the ``wx.EVT_MOVE_END`` event.
        """
        event.GetEventObject().SetTransparent(255)

#----------------------------------------------------------------------------


if __name__ == '__main__':
    # Test App.
    class TopLevelWindowMixinFrame(wx.Frame, TempTransparencyMoveMixin):
        def __init__(self, parent, id=wx.ID_ANY, title=wx.EmptyString,
                     pos=wx.DefaultPosition, size=wx.DefaultSize,
                     style=wx.DEFAULT_FRAME_STYLE, name='frame'):
            wx.Frame.__init__(self, parent, id, title, pos, size, style, name)

            TempTransparencyMoveMixin.__init__(self, 170)

            self.Bind(wx.EVT_CLOSE, self.OnDestroy)

        def OnDestroy(self, event):
            self.Destroy()


    class TopLevelWindowMixinApp(wx.App):
        def OnInit(self):
            gMainWin = TopLevelWindowMixinFrame(None)
            gMainWin.SetTitle('TopLevelWindow Mixin Test')
            self.SetTopWindow(gMainWin)
            gMainWin.Show()
            return True


    gApp = TopLevelWindowMixinApp(redirect=False,
            filename=None,
            useBestVisual=False,
            clearSigInt=True)

    gApp.MainLoop()
