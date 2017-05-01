#!/usr/bin/env python

#----------------------------------------------------------------------------
# Name:        wx.lib.mcow.mixins.listctrl
# Purpose:     Helpful mix-in classes for wx.ListCtrl
#
# Author:      Edward Greig
#
# Created:     25-Jan-2014
# Copyright:   (c) Edward Greig 2014
# Licence:     wxWindows license
#----------------------------------------------------------------------------


import wx


class ListCtrlRowHighlighterMixin:
    """SourceCoder Library: ListCtrlRowHighlighterMixin
    Mixin class that handles automatic background highlighting of rows in
    the a ListCtrl. The background of the rows are highlighted automatically
    as items are added or inserted in the control based on the set Colors list.
    Colors will appear in the order they are in the set Colors list.

    """
    def __init__(self, colors=None, reverseForeground=False):
        """Initialize the highlighter mixin
        :param `colors`: list of colors >= 2 to set custom highlight colors
        :param `reverseForeground`: bool(default False) apply reverse colors
         list colors as items text color.
        :type `reverseForeground`: bool

        """
        # Attributes
        self._colors = colors
        self._reverseForeground = reverseForeground

        # Event Handlers
        self.Bind(wx.EVT_LIST_INSERT_ITEM, lambda evt: self.HighlightRows())
        self.Bind(wx.EVT_LIST_DELETE_ITEM, lambda evt: self.HighlightRows())

    def HighlightRows(self):
        """Re-color all the rows"""
        colors = [color for color in enumerate(self._colors)]
        lenColors = len(self._colors)
        localSetItemBackgroundColour = self.SetItemBackgroundColour
        [localSetItemBackgroundColour(row, colors[row % lenColors][1])
            for row in range(self.GetItemCount())]

        if self._reverseForeground:
            colors.reverse()
            localSetItemTextColour = self.SetItemTextColour
            [localSetItemTextColour(row, colors[row % lenColors][1])
                for row in range(self.GetItemCount())]

    def SetHighlightColors(self, colors):
        """
        Set the colors used to highlight the rows. Call :meth:`HighlightRows`
        after this if you wish to update all the rows highlight colors.

        :param `colors`: tuple or list of colors >= 2 to set default colors
        :type `colors`: tuple or list
        """
        self._colors = colors


if __name__ == '__main__':
    import sys

    class HighlighterListCtrl1(wx.ListCtrl, ListCtrlRowHighlighterMixin):
        def __init__(self, parent, id=wx.ID_ANY,
                     pos=wx.DefaultPosition, size=wx.DefaultSize,
                     style=wx.LC_REPORT, name='listctrl'):
            wx.ListCtrl.__init__(self, parent, id, pos, size, style)

            self.InsertColumn(0, "ListCtrlRowHighlighterMixin")

            for index in range(501):
                self.InsertItem(index, 'Python is the Best! %s' % index)

            self.SetColumnWidth(0, 150)

            ListCtrlRowHighlighterMixin.__init__(self,
                (wx.RED, wx.WHITE, wx.BLUE))
            self.HighlightRows()

    class HighlighterListCtrl2(wx.ListCtrl, ListCtrlRowHighlighterMixin):
        def __init__(self, parent, id=wx.ID_ANY,
                     pos=wx.DefaultPosition, size=wx.DefaultSize,
                     style=wx.LC_REPORT, name='listctrl'):
            wx.ListCtrl.__init__(self, parent, id, pos, size, style)

            self.InsertColumn(0, "ListCtrlRowHighlighterMixin")

            for index in range(501):
                self.InsertItem(index, 'Python is the Best! %s' % index)

            self.SetColumnWidth(0, 150)

            ListCtrlRowHighlighterMixin.__init__(self,
                ['#F39D76', '#F5B57F', '#F9CD8A', '#FFF99D', '#C7E19D', '#A8D59D',
                 '#88C99D', '#8CCCCA', '#8DCFF3', '#93A9D5', '#9595C5', '#9681B6',
                 '#AF88B8', '#C78FB9', '#F59FBC', '#F49E9C'])
            self.HighlightRows()

    class HighlighterListCtrl3(wx.ListCtrl, ListCtrlRowHighlighterMixin):
        def __init__(self, parent, id=wx.ID_ANY,
                     pos=wx.DefaultPosition, size=wx.DefaultSize,
                     style=wx.LC_REPORT, name='listctrl'):
            wx.ListCtrl.__init__(self, parent, id, pos, size, style)

            self.InsertColumn(0, "ListCtrlRowHighlighterMixin")

            for index in range(501):
                self.InsertItem(index, 'Python is the Best! %s' % index)

            self.SetColumnWidth(0, 150)

            ListCtrlRowHighlighterMixin.__init__(self,
                [wx.BLACK, wx.WHITE, wx.BLACK, wx.WHITE], reverseForeground=True)
            self.HighlightRows()

    class ListCtrlRowHighlighterFrame(wx.Frame):
        def __init__(self, parent, id=wx.ID_ANY, title=wx.EmptyString,
                     pos=wx.DefaultPosition, size=wx.DefaultSize,
                     style=wx.DEFAULT_FRAME_STYLE, name='frame'):
            wx.Frame.__init__(self, parent, id, title, pos, size, style, name)

            hbSizer = wx.BoxSizer(wx.HORIZONTAL)
            hbSizer.Add(HighlighterListCtrl1(self, size=(175, -1)), 1, wx.EXPAND | wx.ALL, 5)
            hbSizer.Add(HighlighterListCtrl2(self, size=(175, -1)), 1, wx.EXPAND | wx.ALL, 5)
            hbSizer.Add(HighlighterListCtrl3(self, size=(175, -1)), 1, wx.EXPAND | wx.ALL, 5)
            self.SetSizerAndFit(hbSizer)

            self.Bind(wx.EVT_CLOSE, self.OnDestroy)

            wxVER = 'wxPython %s' % wx.version()
            pyVER = 'python %d.%d.%d.%s' % sys.version_info[0:4]
            versionInfos = '%s %s' % (wxVER, pyVER)
            self.CreateStatusBar().SetStatusText(versionInfos)

        def OnDestroy(self, event):
            self.Destroy()

    class ListCtrlRowHighlighterApp(wx.App):
        def OnInit(self):
            gMainWin = ListCtrlRowHighlighterFrame(None)
            gMainWin.SetTitle('ListCtrlRowHighlighterMixin')
            gMainWin.Show()
            gMainWin.SetSize((-1, 400))
            return True

    gApp = ListCtrlRowHighlighterApp(redirect=False,
            filename=None,
            useBestVisual=False,
            clearSigInt=True)

    gApp.MainLoop()
