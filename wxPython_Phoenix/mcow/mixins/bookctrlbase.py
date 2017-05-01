#!/usr/bin/env python

#----------------------------------------------------------------------------
# Name:        wx.lib.mcow.mixins.bookctrlbase
# Purpose:     Helpful mix-in classes for wx.BookCtrlBase
#
# Author:      Edward Greig
#
# Created:     10-Feb-2014
# Copyright:   (c) Edward Greig 2014
# Licence:     wxWindows license
#----------------------------------------------------------------------------


import wx


class BookCtrlBaseAuxAdvanceMixin:
    """SourceCoder Library: BookCtrlBaseAuxAdvanceMixin
    Mixin class that handles aux mouse button clicking to
    advance forward or backward the book pages for :class:`BookCtrlBase`
    subclasses.

    Example Usage:
        import wx
        from wx.lib.mcow.mixins.bookctrlbase import BookCtrlBaseAuxAdvanceMixin

        class TestTextCtrl(wx.TextCtrl, BookCtrlBaseAuxAdvanceMixin):
            def __init__(self, parent, id=wx.ID_ANY):
                wx.TextCtrl.__init__(self, parent, id)

                BookCtrlBaseAuxAdvanceMixin.__init__(self)

        app = wx.App(0)
        app.frame = wx.Frame(None)
        app.frame.notebook = wx.Notebook(app.frame)
        for i in range(9):
            tc = TestTextCtrl(app.frame.notebook)
            tc.SetValue('Page %d' % i)
            app.frame.notebook.AddPage(tc, 'Page %d' % i)
        app.frame.Show(True)
        app.MainLoop()
    """
    def __init__(self):
        """Initialize the BookCtrlBaseAuxAdvanceMixin mixin"""

        # Event Handlers.
        if not hasattr(self.GetParent(), 'AdvanceSelection'):
            print('\a') # Sound the system bell.
            raise Exception('class %s ' % self.__class__.__name__ +
                            'parent must be a subclass of BookCtrlBase.\n' +
                            'Example Subclasses: AuiNotebook, Choicebook, Listbook, Notebook, Simplebook, Toolbook, Treebook')
        self._bookctrlbase_instance_AuxAdvanceMixin = self.GetParent()

        ## self.Bind(wx.EVT_MOUSE_AUX1_DCLICK, self.OnMouseAux1DClick_BookCtrlBaseAuxAdvanceMixin)
        self.Bind(wx.EVT_MOUSE_AUX1_DOWN, self.OnMouseAux1Down_BookCtrlBaseAuxAdvanceMixin)
        ## self.Bind(wx.EVT_MOUSE_AUX1_UP, self.OnMouseAux1Up_BookCtrlBaseAuxAdvanceMixin)
        ## self.Bind(wx.EVT_MOUSE_AUX2_DCLICK, self.OnMouseAux2DClick_BookCtrlBaseAuxAdvanceMixin)
        self.Bind(wx.EVT_MOUSE_AUX2_DOWN, self.OnMouseAux2Down_BookCtrlBaseAuxAdvanceMixin)
        ## self.Bind(wx.EVT_MOUSE_AUX2_UP, self.OnMouseAux2Up_BookCtrlBaseAuxAdvanceMixin)

    def OnMouseAux1Down_BookCtrlBaseAuxAdvanceMixin(self, event):
        """
        Cycles backwards through the tabs.
        """
        self._bookctrlbase_instance_AuxAdvanceMixin.AdvanceSelection(False)

    ## def OnMouseAux1Up_BookCtrlBaseAuxAdvanceMixin(self, event):
    ##     pass

    def OnMouseAux2Down_BookCtrlBaseAuxAdvanceMixin(self, event):
        """
        Cycles forwards through the tabs.
        """
        self._bookctrlbase_instance_AuxAdvanceMixin.AdvanceSelection(True)

    ## def OnMouseAux2Up_BookCtrlBaseAuxAdvanceMixin(self, event):
    ##     pass
    ##
    ## def OnMouseAux1DClick_BookCtrlBaseAuxAdvanceMixin(self, event):
    ##     pass
    ##
    ## def OnMouseAux2DClick_BookCtrlBaseAuxAdvanceMixin(self, event):
    ##     pass


if __name__ == '__main__':
    # Test app.
    print('wxPython %s' % wx.version())

    import sys
    import wx.lib.agw.aui
    from wx.lib.embeddedimage import PyEmbeddedImage
    snakey16 = PyEmbeddedImage(
        "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAZklEQVR4AWOgFvhPJkYYIPpf"
        "8r/Kf7X/Jv/N/rv+d/sf8T/qf87/vP/1/xv/T/4/5f/y/yvgGm8DIVkG7ALC00AIMgCoG4yR"
        "DSDN+VADyHUBpheIx5SHAU4DyI9G+ofBaBggMDUAAAWBbiUaIpU/AAAAAElFTkSuQmCC")

    class TestTextCtrl(wx.TextCtrl, BookCtrlBaseAuxAdvanceMixin):
        def __init__(self, parent, id=wx.ID_ANY, value=wx.EmptyString,
                     pos=wx.DefaultPosition, size=wx.DefaultSize,
                     style=wx.TE_MULTILINE, name='textctrl'):
            wx.TextCtrl.__init__(self, parent, id, value, pos, size, style)

            BookCtrlBaseAuxAdvanceMixin.__init__(self)

    class TestBookCtrlBaseMixinsFrame(wx.Frame):
        def __init__(self, parent, id=wx.ID_ANY, title=wx.EmptyString,
                     pos=wx.DefaultPosition, size=wx.DefaultSize,
                     style=wx.DEFAULT_FRAME_STYLE, name='frame'):
            wx.Frame.__init__(self, parent, id, title, pos, size, style, name)

            self.Bind(wx.EVT_CLOSE, self.OnDestroy)

        def OnDestroy(self, event):
            self.Destroy()

    class TestBookCtrlBaseMixinsApp(wx.App):
        def OnInit(self):
            bookCtrls = [
                    'wx.Choicebook',
                    'wx.Listbook',
                    'wx.Notebook',
                    'wx.Toolbook',
                    'wx.Treebook',
                    'wx.lib.agw.aui.AuiNotebook'
                    ]
            if 'phoenix' in wx.version():
                bookCtrls.insert(0, 'wx.BookCtrl')
            for bookctrl in bookCtrls:
                frame = TestBookCtrlBaseMixinsFrame(None)
                frame.bookCtrl = eval('%s(frame, -1)' % bookctrl)

                if bookctrl in ('wx.Toolbook'):
                    il = wx.ImageList(32, 32)
                    for i in range(9):
                        img = snakey16.GetImage()
                        img = img.Rescale(32, 32, wx.IMAGE_QUALITY_NEAREST)
                        s = '0.%d' % i
                        img.RotateHue(float(s))
                        bmp = img.ConvertToBitmap()
                        il.Add(bmp)
                    frame.bookCtrl.AssignImageList(il)

                for i in range(9):
                    tc = TestTextCtrl(frame.bookCtrl)
                    tc.SetValue((('%s\n' % bookctrl +
                                  'BookCtrlBaseAuxAdvanceMixin\n' +
                                  'Page %s\n\n' % i) * 10))
                    if bookctrl in ('wx.Toolbook'):
                        frame.bookCtrl.AddPage(tc, 'Page %d' % i, imageId=i)
                    else:
                        frame.bookCtrl.AddPage(tc, 'Page %d' % i)
                frame.SetTitle('%s BookCtrlBaseAuxAdvanceMixin' % bookctrl)
                frame.SetSize((-1, 350))

                wxVER = 'wxPython %s' % wx.version()
                pyVER = 'python %d.%d.%d.%s' % sys.version_info[0:4]
                versionInfos = '%s %s' % (wxVER, pyVER)
                frame.CreateStatusBar().SetStatusText(versionInfos)

                frame.Show()
            return True

    gApp = TestBookCtrlBaseMixinsApp(redirect=False,
            filename=None,
            useBestVisual=False,
            clearSigInt=True)

    gApp.MainLoop()
