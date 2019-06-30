#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
theclipboard.py
===============

wx.TheClipboard functions.

"""

# Imports.--------------------------------------------------------------------
# -wxPython Imports.
import wx


def GetTheClipboardText():
    """
    Get TheClipbboard Text.

    :returns: The clipboard text if successful else False.
    """
    if not wx.TheClipboard.IsOpened():
        wx.TheClipboard.Open()
    text = wx.TextDataObject()
    successful = wx.TheClipboard.GetData(text)
    wx.TheClipboard.Close()
    if successful:
        return text.GetText()
    return False


def SetTheClipboardText(text):
    """
    Set TheClipbboard Text.

    :returns: Whether or not setting the clipboard text was successful.
    :rtype: bool
    """
    data = wx.TextDataObject()
    data.SetText(text)
    if not wx.TheClipboard.IsOpened():
        wx.TheClipboard.Open()
    successful = wx.TheClipboard.SetData(data)
    wx.TheClipboard.Close()
    if successful:
        return True
    return False


def FlushTheClipboard():
    """
    Preserve the clipboard contents.

    Flushes the clipboard: this means that the data which is currently on
    clipboard will stay available even after the application exits,
    possibly eating memory, otherwise the clipboard will be emptied on
    exit.

    :returns: False if the operation is unsuccesful for any reason.
    :rtype: bool
    """
    return wx.TheClipboard.Flush()


if __name__ == '__main__':
    import sys
    import wx
    class TheClipboardFrame(wx.Frame):
        """"""
        def __init__(self, parent, id=wx.ID_ANY, title=wx.EmptyString,
                     pos=wx.DefaultPosition, size=wx.DefaultSize,
                     style=wx.DEFAULT_FRAME_STYLE, name='frame'):
            """"""
            wx.Frame.__init__(self, parent, id, title, pos, size, style, name)
            wxVER = 'wxPython %s' % wx.version()
            pyVER = 'python %d.%d.%d.%s' % sys.version_info[0:4]
            versionInfos = '%s %s' % (wxVER, pyVER)
            self.CreateStatusBar().SetStatusText(versionInfos)
            tc = wx.TextCtrl(self, -1, value='My Text', style=wx.TE_MULTILINE)
            self.btn1 = wx.Button(self, -1, 'GetTheClipboardText')
            self.btn2 = wx.Button(self, -1, 'SetTheClipboardText("Test")')

            self.btn1.Bind(wx.EVT_BUTTON, self.OnButton)
            self.btn2.Bind(wx.EVT_BUTTON, self.OnButton)
            vbSizer = wx.BoxSizer(wx.VERTICAL)
            vbSizer.Add(tc, 1, wx.EXPAND | wx.ALL, 0)
            vbSizer.Add(self.btn1, 0, wx.EXPAND | wx.ALL, 0)
            vbSizer.Add(self.btn2, 0, wx.EXPAND | wx.ALL, 0)
            self.SetSizer(vbSizer)

            self.Bind(wx.EVT_CLOSE, self.OnDestroy)

        def OnButton(self, event):
            if event.GetEventObject() == self.btn1:
                print(GetTheClipboardText())
            elif event.GetEventObject() == self.btn2:
                print(SetTheClipboardText("Test"))

        def OnDestroy(self, event):
            print("Flushing the clipboard = %s" % FlushTheClipboard())
            self.Destroy()

    class TheClipboardApp(wx.App):
        def OnInit(self):
            gMainWin = TheClipboardFrame(None)
            gMainWin.SetTitle('TheClipboard Test Frame')
            self.SetTopWindow(gMainWin)
            gMainWin.Center()
            gMainWin.Show()
            return True


    gApp = TheClipboardApp(redirect=False,
                           filename=None,
                           useBestVisual=False,
                           clearSigInt=True)
    gApp.MainLoop()
