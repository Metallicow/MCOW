#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
ScrolledTextCtrlMessageDialog
=============================

This class is a possible replacement for :class:`MessageDialog`
simple OK style dialogs.

Description
-----------

Generic scrolled TextCtrl message dialog.

* Supports background and foreground colors.
* Supports hyperlinks.
* Good old Python code :)

Usage
-----

Usage example::

    import wx
    import wx.lib.mcow.dialogs as PYDLG

    # Our normal wxApp-derived class, as usual
    app = wx.App(0)

    message = ("Hello world! I am the dialog message."
               "\n\n"
               "Supports hyperlinks too!"
               "\n\n"
               "http://wxpython.org/")
    caption = "A Nice Message Box"
    dlg = PYDLG.ScrolledTextCtrlMessageDialog(None, message, caption)

    dlg.ShowModal()
    dlg.Destroy()

    app.MainLoop()


License And Version
-------------------

`ScrolledTextCtrlMessageDialog` is distributed under the wxPython license.

(c) Edward Greig, @ 27 Jan 2018

"""


# Imports----------------------------------------------------------------------

# -Python Imports.
import webbrowser

# -wxPython Imports.
import wx

_ = wx.GetTranslation


class ScrolledTextCtrlMessageDialog(wx.Dialog):
    """
    Main class implementation, :class:`ScrolledTextCtrlMessageDialog` is a
    possible replacement for the standard :class:`MessageDialog`
    simple OK style dialogs.

    Subclass of `wx.Dialog <http://wxpython.org/Phoenix/docs/html/wx.Dialog.html>`_
    """
    def __init__(self, parent, message='', caption='',
                 pos=wx.DefaultPosition, size=wx.DefaultSize,
                 style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER,
                 bgColor=wx.NullColour, fgColor=wx.NullColour,
                 id=wx.ID_ANY, name='dialog'):
        """
        Default class constructor.

        :param `parent`: Pointer to a parent window. Can be ``None``, a frame or another dialog box.
        :type `parent`: `wx.Window`
        :param `message`: The message text for the dialog.
        :type `message`: str
        :param `caption`: The title of the dialog.
        :type `caption`: str
        :param `pos`: The dialog position. The value ``wx.DefaultPosition`` indicates a default position, chosen by either the windowing system or wxWidgets, depending on platform.
        :type `pos`: `wx.Point`
        :param `size`: The dialog size. The value ``wx.DefaultSize`` indicates a default size, chosen by either the windowing system or wxWidgets, depending on platform.
        :type `size`: `wx.Size`
        :param `style`: The window style.
        :type `style`: long
        :param `bgColor`: The background color.
        :type `bgColor`: `wx.Colour`
        :param `fgColor`: The foreground color.
        :type `fgColor`: `wx.Colour`
        :param `id`: Window identifier. ``wx.ID_ANY`` indicates a default value.
        :type `id`: int
        :param `name`: Used to associate a name with the window, allowing the application user to set Motif resource values for individual dialog boxes.
        :type `name`: str
        """
        wx.Dialog.__init__(self, parent, id, caption, pos, size, style, name)
        self.SetExtraStyle(wx.DIALOG_EX_CONTEXTHELP)
        posX, posY = pos
        defPosX, defPosY = wx.DefaultPosition
        if posX == defPosX and posY == defPosY:
            self.CenterOnScreen(wx.BOTH)

        self.gTextCtrl = tc = wx.TextCtrl(self, wx.ID_ANY, '',
                                          style=wx.BORDER_SUNKEN |
                                                wx.TE_MULTILINE |
                                                wx.TE_NOHIDESEL |
                                                wx.TE_RICH2 | wx.TE_AUTO_URL |
                                                wx.TE_READONLY
                                                )
        # In case user for example creates the dialog then sets the font
        # on the dialog or the textctrl(maybe the user needs a mono font...)
        # we need to update the message so the auto url shows up and works right.
        # so we will override SetFont.
        tc.SetFont = self.SetFont
        tc.SetValue(message)  # Update AutoURL after creation.
        tc.Bind(wx.EVT_TEXT_URL, self.OnTextURL)
        tc.SetHelpText(_(u'This is the scrolled message dialog text.'))
        tc.SetBackgroundColour(bgColor)
        tc.SetForegroundColour(fgColor)

        self.gOKButton = btn = wx.Button(self, wx.ID_OK, _(u'OK'))
        btn.Bind(wx.EVT_BUTTON, self.OnClose)
        btn.SetHelpText(_(u'Clicking the "OK" button will close the dialog.'))
        btn.SetDefault()
        self.Bind(wx.EVT_CLOSE, self.OnClose)

        self.SetHelpText(_(u'This is a scrolled message dialog.'))

        self.DoLayout()

    def DoLayout(self):
        """Do sizer layout for :class:`ScrolledTextCtrlMessageDialog`."""
        vbSizer0 = wx.BoxSizer(wx.VERTICAL)
        vbSizer0.Add(self.gTextCtrl, 1, wx.EXPAND | wx.ALL, 3)
        vbSizer0.Add(self.gOKButton, 0, wx.ALIGN_CENTRE_HORIZONTAL | wx.ALL, 3)
        self.SetSizer(vbSizer0)

    def SetFont(self, font):
        """
        Sets the font for this window.

        SetFont(self, Font font) -> bool

        :param `font`:
        :type `font`: `wx.Font`
        :returns: Whether the font was successfully set.
        :rtype: bool
        """
        boolean = super(wx.TextCtrl, self.gTextCtrl).SetFont(font)
        self.gTextCtrl.SetValue(self.gTextCtrl.GetValue())
        return boolean

    def OnTextURL(self, event):
        """
        Handles the ``wx.EVT_TEXT_URL`` event for :attr:`gTextCtrl`

        :param `event`: A `wx.TextURLEvent` to be processed.
        :type `event`: `wx.TextURLEvent`
        """
        mouseEvent = event.GetMouseEvent()
        if mouseEvent.LeftDClick():
            urlStart = event.GetURLStart()
            urlEnd = event.GetURLEnd()
            url = self.gTextCtrl.GetRange(urlStart, urlEnd)
            webbrowser.open_new_tab(url)

    def OnClose(self, event):
        """
        Handles the ``wx.EVT_CLOSE`` event for :class:`ScrolledTextCtrlMessageDialog`
        Handles the ``wx.EVT_BUTTON`` event for :attr:`gOKButton`

        Close the dialog and return code ``wx.ID_OK`` if modal.

        :param `event`: A `wx.CloseEvent` or `wx.CommandEvent` to be processed.
        :type `event`: `wx.CloseEvent` or `wx.CommandEvent`
        """
        if self.IsModal():
            self.SetReturnCode(wx.ID_OK)
            returnCode = wx.ID_OK
            self.EndModal(returnCode)
        else:
            self.Hide()
            self.Destroy()


if __name__ == '__main__':
    # Test app
    app = wx.App(0)

    message = ("Hello world! I am the dialog message."
               "\n\n"
               "Supports hyperlinks too!"
               "\n\n"
               "http://wxpython.org/")
    caption = "A Nice Message Box"
    dlg = ScrolledTextCtrlMessageDialog(None, message, caption)
    dlg.ShowModal()
    dlg.Destroy()

    app.MainLoop()

