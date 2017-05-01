#!/usr/bin/env python

# --------------------------------------------------------------------------------- #
# COLORMIXER wxPython IMPLEMENTATION
#
# (c) Edward Greig, @ 6 Oct 2015 - ColorMixer
# Latest Revision: Edward Greig @ 6 Oct 2015, 21.00 GMT
#
#
# TODO List
#
# 0. Any ideas?
# 1. Alpha slider
#
# For All Kind Of Problems, Requests Of Enhancements And Bug Reports, Please
# Write To Us At:
#
# metaliobovinus@gmail.com
#
# Or, Obviously, To The wxPython Mailing List!!!
#
#
# End Of Comments
# --------------------------------------------------------------------------------- #

"""
wx.lib.mcow.colormixer
======================
:class:`ColorMixer` is a color mixing panel.


Description
-----------

The :class:`ColorMixer` is a color mixing panel.



Usage
-----

Usage example::

    import wx
    import wx.lib.mcow.colormixer as colormixer

    class MyFrame(wx.Frame):

        def __init__(self, parent):

            wx.Frame.__init__(self, parent, -1, "ColorMixer Demo")

            colorMixer = colormixer.ColorMixer(self)

    # our normal wxApp-derived class, as usual

    app = wx.App(0)

    frame = MyFrame(None)
    app.SetTopWindow(frame)
    frame.Show()

    app.MainLoop()



Supported Platforms
-------------------

:class:`ColorMixer` has been tested on the following platforms:
  * Windows (Windows 7);


License And Version
-------------------

:class:`ColorMixer` is distributed under the wxPython license.

| (c) Edward Greig, @ 6 Oct 2015 - ColorMixer

Latest Revision: Edward Greig @ 6 Oct 2015, 21.00 GMT

Version 0.2

"""

# Imports.--------------------------------------------------------------------
# -Python Imports.
import random

# -wxPython Imports.
import wx

_ = wx.GetTranslation


class ColorMixer(wx.Panel):
    """
    `ColorMixer` is a color mixing panel.
    """
    def __init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, 
                 size=wx.DefaultSize, style=wx.TAB_TRAVERSAL | wx.CLIP_CHILDREN, 
                 name='panel'):
        """
        Default class constructor.

        :param `parent`: Pointer to a parent window. Must not be ``None``.
        :type `parent`: `wx.Window`_
        :param `id`: Window identifier. ``wx.ID_ANY`` indicates a default value.
        :type `id`: int
        :param `pos`: Window position. The value ``wx.DefaultPosition`` indicates a default position, chosen by either the windowing system or wxWidgets, depending on platform.
        :type `pos`: `wx.Point`_
        :param `size`: Window size. The value ``wx.DefaultSize`` indicates a default size, chosen by either the windowing system or wxWidgets, depending on platform.
        :type `size`: `wx.Size`_
        :param `style`: Window style.
        :type `style`: long
        :param `name`: Window name.
        :type `name`: str
        """
        wx.Panel.__init__(self, parent, id, pos, size, style, name)

        self.SetDoubleBuffered(True)

        ID_RED = wx.NewId()
        ID_GREEN = wx.NewId()
        ID_BLUE = wx.NewId()

        slSty = wx.SL_HORIZONTAL | wx.SL_AUTOTICKS# | wx.SL_LABELS
        self.rSt = wx.StaticText(self, wx.ID_ANY, label='128 = 80')
        self.rSl = wx.Slider(self, ID_RED, value=128, minValue=0, maxValue=255,
            size=(256, -1), style=slSty)
        self.rSl.SetTickFreq(16)
        self.rSl.SetBackgroundColour(wx.RED)
        self.rSl.Bind(wx.EVT_SLIDER, self.OnSlider)

        self.gSt = wx.StaticText(self, wx.ID_ANY, label='128 = 80')
        self.gSl = wx.Slider(self, ID_GREEN, value=128, minValue=0, maxValue=255,
            size=(256, -1), style=slSty)
        self.gSl.SetTickFreq(16)
        self.gSl.SetBackgroundColour(wx.GREEN)
        self.gSl.Bind(wx.EVT_SLIDER, self.OnSlider)

        self.bSt = wx.StaticText(self, wx.ID_ANY, label='128 = 80')
        self.bSl = wx.Slider(self, ID_BLUE, value=128, minValue=0, maxValue=255,
            size=(256, -1), style=slSty)
        self.bSl.SetTickFreq(16)
        self.bSl.SetBackgroundColour(wx.BLUE)
        self.bSl.Bind(wx.EVT_SLIDER, self.OnSlider)

        self.colorWin = wx.Window(self, wx.ID_ANY, size=(200, 200), style=wx.BORDER_SIMPLE)
        self.colorWin.SetBackgroundColour((128, 128, 128))

        self.sync = wx.RadioBox(self, wx.ID_ANY, _(u"Synchronize"),
                                choices=[_(u'None'), _(u'RGB'), _(u'RG'), _(u'RB'), _(u'GB')])
        self.sync.Bind(wx.EVT_RADIOBOX, self.OnSynchronize)

        btn = wx.Button(self, wx.ID_ANY, _(u"Randomize"))
        btn.Bind(wx.EVT_BUTTON, self.OnRandomize)

        self.hexTxt = wx.TextCtrl(self, -1, '#808080', style=wx.TE_READONLY)

        vbSizer = wx.BoxSizer(wx.VERTICAL)
        b = 3
        vbSizer.Add(self.rSt, 0, wx.ALIGN_CENTRE_HORIZONTAL | wx.ALL, b)
        vbSizer.Add(self.rSl, 0, wx.EXPAND | wx.ALL, b)
        vbSizer.Add(self.gSt, 0, wx.ALIGN_CENTRE_HORIZONTAL | wx.ALL, b)
        vbSizer.Add(self.gSl, 0, wx.EXPAND | wx.ALL, b)
        vbSizer.Add(self.bSt, 0, wx.ALIGN_CENTRE_HORIZONTAL | wx.ALL, b)
        vbSizer.Add(self.bSl, 0, wx.EXPAND | wx.ALL, b)

        hbSizer1 = wx.BoxSizer(wx.HORIZONTAL)
        hbSizer1.Add(vbSizer, 0, wx.ALIGN_CENTRE_VERTICAL | wx.ALL, b)
        hbSizer1.Add(self.colorWin, 0, wx.ALIGN_CENTRE_VERTICAL | wx.ALL, b)

        hbSizer2 = wx.BoxSizer(wx.HORIZONTAL)
        hbSizer2.Add(self.sync, 0, wx.ALIGN_CENTRE_VERTICAL | wx.ALL, b)
        hbSizer2.Add(btn, 0, wx.ALIGN_CENTRE_VERTICAL | wx.ALL, b)
        hbSizer2.Add(self.hexTxt, 0, wx.ALIGN_CENTRE_VERTICAL | wx.ALL, b)

        main_vbSizer = wx.BoxSizer(wx.VERTICAL)
        main_vbSizer.Add(hbSizer1, 0, wx.ALIGN_CENTRE_HORIZONTAL | wx.ALL, b)
        main_vbSizer.Add(hbSizer2, 0, wx.ALIGN_CENTRE_HORIZONTAL | wx.ALL, b)
        self.SetSizer(main_vbSizer)

    def GetColour(self):
        return self.colorWin.GetBackgroundColour()
        
    def SetColour(self, colour):
        hexidecimal = ('a', 'b', 'c', 'd', 'e', 'f', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0')
        if isinstance(colour, wx.Colour):
            self.colorWin.SetBackgroundColour(colour)
        elif isinstance(colour, (str, unicode)):
            lenColour = len(colour)
            if lenColour in (3, 6):  # Ex: FAB, FF8000
                for char in colour.lower():
                    if char not in hexidecimal:
                        return False
                if lenColour == 3:
                    colour = '%s%s%s' % (colour[0] * 2, colour[1] * 2, colour[2] * 2)
                self.colorWin.SetBackgroundColour('#%s' % colour)
            elif lenColour in (4, 7) and colour.startswith('#'):  # Ex: #FAB, #FF8000
                for char in colour[1:].lower():
                    if char not in hexidecimal:
                        return False
                if lenColour == 4:
                    colour = '#%s%s%s' % (colour[1] * 2, colour[2] * 2, colour[3] * 2)
                self.colorWin.SetBackgroundColour(colour)
        elif isinstance(colour, (tuple, list)):
            lenColour = len(colour)
            if lenColour != 3:  # Ex: (255, 128, 0) or [255, 128, 0]
                return False
            for i in colour:
                if not isintance(i, int):
                    return False
                elif not (0 <= i <= 255):
                    return False
            self.colorWin.SetBackgroundColour(wx.Colour(colour[0], colour[1], colour[2]))
        try:
            r, g, b = self.colorWin.GetBackgroundColour().Get()
        except ValueError:
            r, g, b, a = self.colorWin.GetBackgroundColour().Get()
        self.rSl.SetValue(r)
        self.gSl.SetValue(g)
        self.bSl.SetValue(b)
        rHex = hex(r)[2:]
        gHex = hex(g)[2:]
        bHex = hex(b)[2:]
        if len(rHex) == 1:
            rHex = '0%s' % rHex
        if len(gHex) == 1:
            gHex = '0%s' % gHex
        if len(bHex) == 1:
            bHex = '0%s' % bHex
        self.rSt.SetLabel('%s = %s' % (r, rHex))
        self.gSt.SetLabel('%s = %s' % (g, gHex))
        self.bSt.SetLabel('%s = %s' % (b, bHex))
        self.hexTxt.SetValue('#%s%s%s' % (rHex, gHex, bHex))
        return True

    def OnSynchronize(self, event=None):
        syncsel = self.sync.GetSelection()
        rVal = self.rSl.GetValue()
        gVal = self.gSl.GetValue()
        bVal = self.bSl.GetValue()
        rHex = hex(rVal)[2:]
        gHex = hex(gVal)[2:]
        bHex = hex(bVal)[2:]
        if len(rHex) == 1:
            rHex = '0%s' % rHex
        if len(gHex) == 1:
            gHex = '0%s' % gHex
        if len(bHex) == 1:
            bHex = '0%s' % bHex

        if syncsel == 0:  # None
            pass
        elif syncsel == 1:  # RGB
            self.colorWin.SetBackgroundColour((rVal, rVal, rVal))
            self.colorWin.Refresh()
            self.rSt.SetLabel('%s = %s' % (rVal, rHex))
            self.gSt.SetLabel('%s = %s' % (rVal, rHex))
            self.bSt.SetLabel('%s = %s' % (rVal, rHex))
            self.hexTxt.SetValue('#%s%s%s' % (rHex, rHex, rHex))
            self.rSl.SetValue(rVal)
            self.gSl.SetValue(rVal)
            self.bSl.SetValue(rVal)
        elif syncsel == 2:  # RG
            self.colorWin.SetBackgroundColour((rVal, rVal, bVal))
            self.colorWin.Refresh()
            self.rSt.SetLabel('%s = %s' % (rVal, rHex))
            self.gSt.SetLabel('%s = %s' % (rVal, rHex))
            self.bSt.SetLabel('%s = %s' % (bVal, bHex))
            self.hexTxt.SetValue('#%s%s%s' % (rHex, rHex, bHex))
            self.rSl.SetValue(rVal)
            self.gSl.SetValue(rVal)
            self.bSl.SetValue(bVal)
        elif syncsel == 3:  # RB
            self.colorWin.SetBackgroundColour((rVal, gVal, rVal))
            self.colorWin.Refresh()
            self.rSt.SetLabel('%s = %s' % (rVal, rHex))
            self.gSt.SetLabel('%s = %s' % (gVal, gHex))
            self.bSt.SetLabel('%s = %s' % (rVal, rHex))
            self.hexTxt.SetValue('#%s%s%s' % (rHex, gHex, rHex))
            self.rSl.SetValue(rVal)
            self.gSl.SetValue(gVal)
            self.bSl.SetValue(rVal)
        elif syncsel == 4:  # GB
            self.colorWin.SetBackgroundColour((rVal, gVal, gVal))
            self.colorWin.Refresh()
            self.rSt.SetLabel('%s = %s' % (rVal, rHex))
            self.gSt.SetLabel('%s = %s' % (gVal, gHex))
            self.bSt.SetLabel('%s = %s' % (gVal, gHex))
            self.hexTxt.SetValue('#%s%s%s' % (rHex, gHex, gHex))
            self.rSl.SetValue(rVal)
            self.gSl.SetValue(gVal)
            self.bSl.SetValue(gVal)
        # print('syncsel = %s' % syncsel)

    def OnSlider(self, event):
        syncsel = self.sync.GetSelection()
        evtObj = event.GetEventObject()
        rVal = self.rSl.GetValue()
        gVal = self.gSl.GetValue()
        bVal = self.bSl.GetValue()
        rHex = hex(rVal)[2:]
        gHex = hex(gVal)[2:]
        bHex = hex(bVal)[2:]
        if len(rHex) == 1:
            rHex = '0%s' % rHex
        if len(gHex) == 1:
            gHex = '0%s' % gHex
        if len(bHex) == 1:
            bHex = '0%s' % bHex

        if syncsel == 0:  # None
            self.colorWin.SetBackgroundColour((rVal, gVal, bVal))
            self.colorWin.Refresh()
            self.rSt.SetLabel('%s = %s' % (rVal, rHex))
            self.gSt.SetLabel('%s = %s' % (gVal, gHex))
            self.bSt.SetLabel('%s = %s' % (bVal, bHex))
            self.hexTxt.SetValue('#%s%s%s' % (rHex, gHex, bHex))
        elif syncsel == 1:  # RGB
            if evtObj == self.rSl:
                self.rSl.SetValue(rVal)
                self.gSl.SetValue(rVal)
                self.bSl.SetValue(rVal)
                self.colorWin.SetBackgroundColour((rVal, rVal, rVal))
                self.colorWin.Refresh()
                self.rSt.SetLabel('%s = %s' % (rVal, rHex))
                self.gSt.SetLabel('%s = %s' % (rVal, rHex))
                self.bSt.SetLabel('%s = %s' % (rVal, rHex))
                self.hexTxt.SetValue('#%s%s%s' % (rHex, rHex, rHex))
            elif evtObj == self.gSl:
                self.rSl.SetValue(gVal)
                self.gSl.SetValue(gVal)
                self.bSl.SetValue(gVal)
                self.colorWin.SetBackgroundColour((gVal, gVal, gVal))
                self.colorWin.Refresh()
                self.rSt.SetLabel('%s = %s' % (gVal, gHex))
                self.gSt.SetLabel('%s = %s' % (gVal, gHex))
                self.bSt.SetLabel('%s = %s' % (gVal, gHex))
                self.hexTxt.SetValue('#%s%s%s' % (gHex, gHex, gHex))
            elif evtObj == self.bSl:
                self.rSl.SetValue(bVal)
                self.gSl.SetValue(bVal)
                self.bSl.SetValue(bVal)
                self.colorWin.SetBackgroundColour((bVal, bVal, bVal))
                self.colorWin.Refresh()
                self.rSt.SetLabel('%s = %s' % (bVal, bHex))
                self.gSt.SetLabel('%s = %s' % (bVal, bHex))
                self.bSt.SetLabel('%s = %s' % (bVal, bHex))
                self.hexTxt.SetValue('#%s%s%s' % (bHex, bHex, bHex))
        elif syncsel == 2:  # RG
            if evtObj == self.rSl:
                self.rSl.SetValue(rVal)
                self.gSl.SetValue(rVal)
                self.bSl.SetValue(bVal)
                self.colorWin.SetBackgroundColour((rVal, rVal, bVal))
                self.colorWin.Refresh()
                self.rSt.SetLabel('%s = %s' % (rVal, rHex))
                self.gSt.SetLabel('%s = %s' % (rVal, rHex))
                self.bSt.SetLabel('%s = %s' % (bVal, bHex))
                self.hexTxt.SetValue('#%s%s%s' % (rHex, rHex, bHex))
            elif evtObj == self.gSl:
                self.rSl.SetValue(gVal)
                self.gSl.SetValue(gVal)
                self.bSl.SetValue(bVal)
                self.colorWin.SetBackgroundColour((gVal, gVal, bVal))
                self.colorWin.Refresh()
                self.rSt.SetLabel('%s = %s' % (gVal, gHex))
                self.gSt.SetLabel('%s = %s' % (gVal, gHex))
                self.bSt.SetLabel('%s = %s' % (bVal, bHex))
                self.hexTxt.SetValue('#%s%s%s' % (gHex, gHex, bHex))
            elif evtObj == self.bSl:
                self.rSl.SetValue(rVal)
                self.gSl.SetValue(gVal)
                self.bSl.SetValue(bVal)
                self.colorWin.SetBackgroundColour((rVal, gVal, bVal))
                self.colorWin.Refresh()
                self.rSt.SetLabel('%s = %s' % (rVal, rHex))
                self.gSt.SetLabel('%s = %s' % (gVal, gHex))
                self.bSt.SetLabel('%s = %s' % (bVal, bHex))
                self.hexTxt.SetValue('#%s%s%s' % (rHex, gHex, bHex))
        elif syncsel == 3:  # RB
            if evtObj == self.rSl:
                self.rSl.SetValue(rVal)
                self.gSl.SetValue(gVal)
                self.bSl.SetValue(rVal)
                self.colorWin.SetBackgroundColour((rVal, gVal, rVal))
                self.colorWin.Refresh()
                self.rSt.SetLabel('%s = %s' % (rVal, rHex))
                self.gSt.SetLabel('%s = %s' % (gVal, gHex))
                self.bSt.SetLabel('%s = %s' % (rVal, rHex))
                self.hexTxt.SetValue('#%s%s%s' % (rHex, gHex, rHex))
            elif evtObj == self.gSl:
                self.rSl.SetValue(rVal)
                self.gSl.SetValue(gVal)
                self.bSl.SetValue(bVal)
                self.colorWin.SetBackgroundColour((rVal, gVal, bVal))
                self.colorWin.Refresh()
                self.rSt.SetLabel('%s = %s' % (rVal, rHex))
                self.gSt.SetLabel('%s = %s' % (gVal, gHex))
                self.bSt.SetLabel('%s = %s' % (bVal, bHex))
                self.hexTxt.SetValue('#%s%s%s' % (rHex, gHex, bHex))
            elif evtObj == self.bSl:
                self.rSl.SetValue(bVal)
                self.gSl.SetValue(gVal)
                self.bSl.SetValue(bVal)
                self.colorWin.SetBackgroundColour((bVal, gVal, bVal))
                self.colorWin.Refresh()
                self.rSt.SetLabel('%s = %s' % (bVal, bHex))
                self.gSt.SetLabel('%s = %s' % (gVal, gHex))
                self.bSt.SetLabel('%s = %s' % (bVal, bHex))
                self.hexTxt.SetValue('#%s%s%s' % (bHex, gHex, bHex))
        elif syncsel == 4:  # GB
            if evtObj == self.rSl:
                self.rSl.SetValue(rVal)
                self.gSl.SetValue(gVal)
                self.bSl.SetValue(bVal)
                self.colorWin.SetBackgroundColour((rVal, gVal, bVal))
                self.colorWin.Refresh()
                self.rSt.SetLabel('%s = %s' % (rVal, rHex))
                self.gSt.SetLabel('%s = %s' % (gVal, gHex))
                self.bSt.SetLabel('%s = %s' % (bVal, bHex))
                self.hexTxt.SetValue('#%s%s%s' % (rHex, gHex, bHex))
            elif evtObj == self.gSl:
                self.rSl.SetValue(rVal)
                self.gSl.SetValue(gVal)
                self.bSl.SetValue(gVal)
                self.colorWin.SetBackgroundColour((rVal, gVal, gVal))
                self.colorWin.Refresh()
                self.rSt.SetLabel('%s = %s' % (rVal, rHex))
                self.gSt.SetLabel('%s = %s' % (gVal, gHex))
                self.bSt.SetLabel('%s = %s' % (gVal, gHex))
                self.hexTxt.SetValue('#%s%s%s' % (rHex, gHex, gHex))
            elif evtObj == self.bSl:
                self.rSl.SetValue(rVal)
                self.gSl.SetValue(bVal)
                self.bSl.SetValue(bVal)
                self.colorWin.SetBackgroundColour((rVal, bVal, bVal))
                self.colorWin.Refresh()
                self.rSt.SetLabel('%s = %s' % (rVal, rHex))
                self.gSt.SetLabel('%s = %s' % (bVal, bHex))
                self.bSt.SetLabel('%s = %s' % (bVal, bHex))
                self.hexTxt.SetValue('#%s%s%s' % (rHex, bHex, bHex))
        # print('%s' % event.GetInt())

    def OnRandomize(self, event=None):
        rVal = random.randint(0, 255)
        gVal = random.randint(0, 255)
        bVal = random.randint(0, 255)
        rHex = hex(rVal)[2:]
        gHex = hex(gVal)[2:]
        bHex = hex(bVal)[2:]
        if len(rHex) == 1:
            rHex = '0%s' % rHex
        if len(gHex) == 1:
            gHex = '0%s' % gHex
        if len(bHex) == 1:
            bHex = '0%s' % bHex
        self.colorWin.SetBackgroundColour((rVal, gVal, bVal))
        self.colorWin.Refresh()
        self.rSl.SetValue(rVal)
        self.gSl.SetValue(gVal)
        self.bSl.SetValue(bVal)
        self.rSt.SetLabel('%s = %s' % (rVal, rHex))
        self.gSt.SetLabel('%s = %s' % (gVal, gHex))
        self.bSt.SetLabel('%s = %s' % (bVal, bHex))
        self.hexTxt.SetValue('#%s%s%s' % (rHex, gHex, bHex))


if __name__ == '__main__':
    import os
    import sys

    class MyFrame(wx.Frame):
        def __init__(self, parent):
            wx.Frame.__init__(self, parent, -1, "ColorMixer Demo")
            
            wxVER = 'wxPython %s' % wx.version()
            pyVER = 'python %d.%d.%d.%s' % sys.version_info[0:4]
            versionInfos = '%s %s' % (wxVER, pyVER)
            self.CreateStatusBar().SetStatusText(versionInfos)
            
            colorMixer = ColorMixer(self)
            colorMixer.SetColour('#FF8000')
            
            vbSizer = wx.BoxSizer(wx.VERTICAL)
            vbSizer.Add(colorMixer, 1, wx.EXPAND)
            self.SetSizerAndFit(vbSizer)

    # our normal wxApp-derived class, as usual

    app = wx.App(0)

    frame = MyFrame(None)
    app.SetTopWindow(frame)
    frame.Show()

    app.MainLoop()
    