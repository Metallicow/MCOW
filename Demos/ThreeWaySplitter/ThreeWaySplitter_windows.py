#!/usr/bin/env python
# -*- coding: utf-8 -*-

#-Imports.---------------------------------------------------------------------
#--Python Imports.
import os
import sys

#--wxPython Imports.
import wx

import wx.lib.mcow.threewaysplitter as TWS

__wxPyDemoPanel__ = 'ThreeWaySplitterPanel'

class ThreeWaySplitterPanel(wx.Panel):
    def __init__(self, parent, log=None, id=wx.ID_ANY,
                 pos=wx.DefaultPosition, size=wx.DefaultSize,
                 style=wx.BORDER_SUNKEN, name='panel'):
        wx.Panel.__init__(self, parent, id, pos, size, style, name)
        self.log = log

        tws = TWS.ThreeWaySplitter(self, wx.ID_ANY, agwStyle=wx.SP_LIVE_UPDATE)
        tws.SetLoneSide(wx.SOUTH)

        P2 = wx.Panel(tws, -1, style=wx.BORDER_SUNKEN)
        P2.SetBackgroundColour('#B8FF48')
        P3 = wx.Panel(tws, -1, style=wx.BORDER_SUNKEN)

        tws2 = TWS.ThreeWaySplitter(P3, wx.ID_ANY,agwStyle=wx.SP_LIVE_UPDATE)
        tws2.SetLoneSide(wx.NORTH)
        P4 = wx.Panel(tws2, -1, style=wx.BORDER_SUNKEN)
        P4.SetBackgroundColour('#88122F')
        P5 = wx.Panel(tws2, -1, style=wx.BORDER_SUNKEN)
        P5.SetBackgroundColour('#887444')
        P6 = wx.Panel(tws2, -1, style=wx.BORDER_SUNKEN)
        P6.SetBackgroundColour('#308829')

        tws2.AppendWindow(P4)
        tws2.AppendWindow(P5)
        tws2.AppendWindow(P6)

        vbSizer = wx.BoxSizer(wx.VERTICAL)
        vbSizer.Add(tws2, 1, wx.EXPAND | wx.ALL, 5)
        P3.SetSizerAndFit(vbSizer)

        tws3 = TWS.ThreeWaySplitter(P2, wx.ID_ANY,agwStyle=wx.SP_LIVE_UPDATE)
        tws3.SetLoneSide(wx.EAST)
        P7 = wx.Panel(tws3, -1, style=wx.BORDER_SUNKEN)
        P7.SetBackgroundColour('#3C7188')
        P8 = wx.Panel(tws3, -1, style=wx.BORDER_SUNKEN)
        P8.SetBackgroundColour('#D7ED79')
        P9 = wx.Panel(tws3, -1, style=wx.BORDER_SUNKEN)
        P9.SetBackgroundColour('#B840F5')

        tws3.AppendWindow(P7)
        tws3.AppendWindow(P8)
        tws3.AppendWindow(P9)

        tws4 = TWS.ThreeWaySplitter(tws, wx.ID_ANY,agwStyle=wx.SP_LIVE_UPDATE)
        P10 = wx.Panel(tws4, -1, style=wx.BORDER_SUNKEN)
        P10.SetBackgroundColour('#3037FD')
        P11 = wx.Panel(tws4, -1, style=wx.BORDER_SUNKEN)
        P11.SetBackgroundColour('#000000')
        P12 = wx.Panel(tws4, -1, style=wx.BORDER_SUNKEN)
        P12.SetBackgroundColour('#F5F500')

        tws4.AppendWindow(P10)
        tws4.AppendWindow(P11)
        tws4.AppendWindow(P12)

        vbSizer = wx.BoxSizer(wx.VERTICAL)
        vbSizer.Add(tws3, 1, wx.EXPAND | wx.ALL, 5)
        P2.SetSizerAndFit(vbSizer)

        tws5 = TWS.ThreeWaySplitter(P12, wx.ID_ANY,agwStyle=wx.SP_LIVE_UPDATE)
        P13 = wx.Panel(tws5, -1, style=wx.BORDER_SUNKEN)
        P13.SetBackgroundColour('#C5FDE2')
        P14 = wx.Panel(tws5, -1, style=wx.BORDER_SUNKEN)
        P14.SetBackgroundColour('#DF6C45')
        P15 = wx.Panel(tws5, -1, style=wx.BORDER_SUNKEN)
        P15.SetBackgroundColour('#F5D5D7')

        tws5.AppendWindow(P13)
        tws5.AppendWindow(P14)
        tws5.AppendWindow(P15)

        vbSizer = wx.BoxSizer(wx.VERTICAL)
        vbSizer.Add(tws5, 1, wx.EXPAND | wx.ALL, 5)
        P12.SetSizerAndFit(vbSizer)

        tws.AppendWindow(tws4)
        tws.AppendWindow(P2)
        tws.AppendWindow(P3)

        vbSizer = wx.BoxSizer(wx.VERTICAL)
        vbSizer.Add(tws, 1, wx.EXPAND | wx.ALL, 5)
        self.SetSizer(vbSizer)


class ThreeWaySplitterFrame(wx.Frame):
    def __init__(self, parent, id=wx.ID_ANY, title=wx.EmptyString,
                 pos=wx.DefaultPosition, size=wx.DefaultSize,
                 style=wx.DEFAULT_FRAME_STYLE, name='frame'):
        wx.Frame.__init__(self, parent, id, title, pos, size, style, name)
        global gMainWin
        gMainWin = self
        panel = ThreeWaySplitterPanel(self)
        self.Bind(wx.EVT_CLOSE, self.OnDestroy)

        self.CreateStatusBar().SetStatusText('wxPython %s' % wx.version())

    def OnDestroy(self, event):
        self.Destroy()

class ThreeWaySplitterApp(wx.App):
    def OnInit(self):
        self.SetClassName('ThreeWaySplitterApp')
        self.SetAppName('ThreeWaySplitterApp')
        gMainWin = ThreeWaySplitterFrame(None)
        gMainWin.SetTitle('ThreeWaySplitter Demo')
        self.SetTopWindow(gMainWin)
        gMainWin.Show()
        return True

if __name__ == '__main__':
    gApp = ThreeWaySplitterApp(redirect=False,
            filename=None,
            useBestVisual=False,
            clearSigInt=True)

    gApp.MainLoop()
