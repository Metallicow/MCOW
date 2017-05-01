#!/usr/bin/env python
# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------------- #
# PICTURE wxPython IMPLEMENTATION
#
# (c) Edward Greig, @ 27 Oct 2012 - Picture
#
# For All Kind Of Problems, Requests Of Enhancements And Bug Reports, Please
# Write To Me At:
#
# metaliobovinus at gmail dot com
#
# Or, Obviously, To The wxPython Mailing List!!!
#
#
# End Of Comments
# --------------------------------------------------------------------------- #

"""
Picture
=======

`Picture` is a scalable picture window like ones often used in image viewer
applications. It provides Overscaling and Downscaling toggleable options.
Background Color is customizable and can be a tiled texture if desired.

- Create picture panels that scale quickly and easily without having to
   worry about calculating all the math for the scaling;
- Easily create Picture Album/Viewer widgets.


Usage
=====

Usage example::

    import wx
    import wx.lib.mcow.picture as PIC

    class MyFrame(wx.Frame):
        def __init__(self, parent):
            wx.Frame.__init__(self, parent, -1, "Picture Demo")

            pic = PIC.Picture(self)
            pic.SetPicture(wx.Bitmap("MyPicture.png"))
            vbSizer = wx.BoxSizer(wx.VERTICAL)
            vbSizer.Add(pic, 1, wx.EXPAND | wx.ALL, 5)
            self.SetSizer(vbSizer)

    # our normal wxApp-derived class, as usual

    app = wx.App(0)

    frame = MyFrame(None)
    app.SetTopWindow(frame)
    frame.Show()

    app.MainLoop()


Methods and Settings
====================

With `Picture` you can:

- SetPicture(bitmap);
- allowOverscaling;
- allowDownscaling;
- useBackgroundTexture;


Supported Platforms
===================
:class:`Picture` has been tested on the following platforms:
  * Windows (Windows XP) (Windows 7).


License And Version
-------------------

`Picture` is distributed under the wxPython license.

Edward Greig, @ 27 Oct 2012
Latest revision: Edward Greig @ 5 Dec 2016, 21.00 GMT

Version 0.5

"""


import wx

_ = wx.GetTranslation

class Picture(wx.Window):
    """
    Picture window GUI element that has scaling and image qualty options.
    """
    def __init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=0, name='window',
                 picture=wx.NullBitmap,
                 imageQuality=wx.IMAGE_QUALITY_HIGH, backgroundColor=None,
                 backgroundTextureBmp=wx.NullBitmap):
        """
        Constructs a window, which can be a child of a frame, dialog or any other non-control window.

        :param `parent`: (`wx.Window`) - Pointer to a parent window.
        :param `id`: (int) - Window identifier.
         If ID_ANY, will automatically create an identifier.
        :param `pos`: (`wx.Point`) - Window position.
         DefaultPosition indicates that wxWidgets should generate a default position for the window.
         If using the Window class directly, supply an actual position.
        :param `size`: (`wx.Size`) - Window size.
         DefaultSize indicates that wxWidgets should generate a default size for the window.
         If no suitable size can be found, the window will be sized to 20x20 pixels
         so that the window is visible but obviously not correctly sized.
        :param `style`: (long) - Window style. For generic window styles, please see `wx.Window`.
        :param `name`: (string) - Window name.
        :param `imageQuality`: ImageResizeQuality of the Picture. Default is ``wx.IMAGE_QUALITY_HIGH``
        :type `imageQuality`: One of the following: ``wx.IMAGE_QUALITY_NEAREST``,
         ``wx.IMAGE_QUALITY_BILINEAR``, ``wx.IMAGE_QUALITY_BICUBIC``,
         ``wx.IMAGE_QUALITY_BOX_AVERAGE``, ``wx.IMAGE_QUALITY_NORMAL``, ``wx.IMAGE_QUALITY_HIGH``
        :param `backgroundColor`: Background color for the picture.
        :type `backgroundColor`: A `wx.Colour` or (int(r), int(g), int(b)) tuple
        """
        wx.Window.__init__(self, parent, id, pos, size, style, name)

        self.SetBackgroundStyle(wx.BG_STYLE_PAINT)
        if isinstance(picture, wx.Bitmap):
            self.origbitmap = picture
            self.bitmap = picture
        else:  # Figure out if we can use what was sent in other ways.
            self.origbitmap = self._ConvertifyToPicture(picture)
            self.bitmap = self._ConvertifyToPicture(picture)
        if backgroundColor:
            if isinstance(backgroundColor, tuple):
                self.backgroundColor = wx.Colour(backgroundColor)
            elif isinstance(backgroundColor, wx.Colour):
                self.backgroundColor = wx.Brush(backgroundColor)
            else:
                raise TypeError(_(u'Unknown backgroundColor type'))
                self.backgroundColor = wx.Brush(self.GetBackgroundColour())
        else:
            self.backgroundColor = wx.Brush(self.GetBackgroundColour())

        self.useBackgroundTexture = True
        self.useBackgroundGradient = False

        self.backgroundTextureBmp = wx.NullBitmap
        self.backgroundGradientStops = (wx.BLACK, wx.WHITE)

        self.imageQualityMenuItems = (
            (wx.NewId(), 'wx.IMAGE_QUALITY_NEAREST', _(u'Simplest and fastest algorithm.')),
            (wx.NewId(), 'wx.IMAGE_QUALITY_BILINEAR', _(u'Compromise between wx.IMAGE_QUALITY_NEAREST and wx.IMAGE_QUALITY_BICUBIC.')),
            (wx.NewId(), 'wx.IMAGE_QUALITY_BICUBIC', _(u'Highest quality but slowest execution time.')),
            (wx.NewId(), 'wx.IMAGE_QUALITY_BOX_AVERAGE', _(u'Use surrounding pixels to calculate an average that will be used for new pixels.')),
            (wx.NewId(), 'wx.IMAGE_QUALITY_NORMAL', _(u'Default image resizing algorithm used by wx.Image.Scale .')),
            (wx.NewId(), 'wx.IMAGE_QUALITY_HIGH', _(u'Best image resizing algorithm.')))
        [self.Bind(wx.EVT_MENU, self.OnChangeImageQuality, id=newid) for newid, text, help in self.imageQualityMenuItems]
        self.imageQualityEnums = {
            'wx.IMAGE_QUALITY_NEAREST': wx.IMAGE_QUALITY_NEAREST,
            'wx.IMAGE_QUALITY_BILINEAR': wx.IMAGE_QUALITY_BILINEAR,
            'wx.IMAGE_QUALITY_BICUBIC': wx.IMAGE_QUALITY_BICUBIC,
            'wx.IMAGE_QUALITY_BOX_AVERAGE': wx.IMAGE_QUALITY_BOX_AVERAGE,
            'wx.IMAGE_QUALITY_NORMAL': wx.IMAGE_QUALITY_NORMAL,
            'wx.IMAGE_QUALITY_HIGH': wx.IMAGE_QUALITY_HIGH
            }
        self.imageQuality = imageQuality

        self.allowOverscaling = False
        self.allowDownscaling = True

        # Context Menu Item IDs
        self.ID_TOGGLEALLOWOVERSCALING = wx.NewId()
        self.ID_TOGGLEALLOWDOWNSCALING = wx.NewId()

        #--Events
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_CONTEXT_MENU, self.OnContextMenu)

        self.BindEvents()
        self.OnSize()


    def BindEvents(self):
        """
        Bind various event types for :class:`Picture`.
        """
        self_Bind = self.Bind
        self_Bind(wx.EVT_MENU, self.OnToggleScalingOption, id=self.ID_TOGGLEALLOWOVERSCALING)
        self_Bind(wx.EVT_MENU, self.OnToggleScalingOption, id=self.ID_TOGGLEALLOWDOWNSCALING)
        self_Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)
        self_Bind(wx.EVT_PAINT, self.OnPaint)
        self_Bind(wx.EVT_SIZE, self.OnSize)
        self_Bind(wx.EVT_CONTEXT_MENU, self.OnContextMenu)

    def GetPicturePopupMenu(self):
        """
        Get the built-in popup menu for :class:`Picture`.

        :rtype: A `wx.Menu`
        """
        m = wx.Menu()
        mi = wx.MenuItem(m, self.ID_TOGGLEALLOWOVERSCALING, _(u'Allow Overscaling'), kind=wx.ITEM_CHECK)
        m.Append(mi)
        if self.allowOverscaling:
            mi.Check(True)
        mi = wx.MenuItem(m, self.ID_TOGGLEALLOWDOWNSCALING, _(u'Allow Downscaling'), kind=wx.ITEM_CHECK)
        m.Append(mi)
        if self.allowDownscaling:
            mi.Check(True)

        sm = wx.Menu()
        for tup in self.imageQualityMenuItems:
            mi = wx.MenuItem(m, tup[0], u'%s' % tup[1], u'%s' % tup[2], kind=wx.ITEM_CHECK)
            sm.Append(mi)
            if self.imageQualityEnums[u'%s' % tup[1]] == self.imageQuality:
                mi.Check(True)
        m.AppendSubMenu(sm, _(u'Image Quality'))
        return m

    def OnContextMenu(self, event):
        """
        Handles the ``wx.EVT_CONTEXT_MENU`` event for :class:`Picture`.

        :param `event`: A `wx.ContextMenuEvent` to be processed.
        :type `event`: `wx.ContextMenuEvent`
        """
        m = self.GetPicturePopupMenu()
        self.PopupMenu(m)
        m.Destroy()

    def OnChangeImageQuality(self, event):
        """
        Change the image quality of the scaled picture
        """
        evtId = event.GetId()
        evtMenu = event.GetEventObject()
        for tup in self.imageQualityMenuItems:
            if tup[0] == evtId:
                evtMenuItem = evtMenu.FindItemById(tup[0])
        label = evtMenuItem.GetLabel()
        self.imageQuality = self.imageQualityEnums[label]
        self.OnSize()

    def OnToggleScalingOption(self, event):
        """
        Toggle Overscaling or DownScaling options.
        """
        evtId = event.GetId()
        if evtId == self.ID_TOGGLEALLOWOVERSCALING:
            self.allowOverscaling = not self.allowOverscaling
        elif evtId == self.ID_TOGGLEALLOWDOWNSCALING:
            self.allowDownscaling = not self.allowDownscaling
        self.OnSize()

    def GetImageQuality(self):
        """
        Get the image quality of the scaled picture.

        :returns: One of the following: ``wx.IMAGE_QUALITY_NEAREST``,
         ``wx.IMAGE_QUALITY_BILINEAR``, ``wx.IMAGE_QUALITY_BICUBIC``,
         ``wx.IMAGE_QUALITY_BOX_AVERAGE``, ``wx.IMAGE_QUALITY_NORMAL``,
         ``wx.IMAGE_QUALITY_HIGH``
        """
        return self.imageQuality

    def SetImageQuality(self, imageQuality):
        """
        Set the image quality of the scaled picture.

        :param `imageQuality`: ImageResizeQuality of the Picture.
        :type `imageQuality`: One of the following: ``wx.IMAGE_QUALITY_NEAREST``,
         ``wx.IMAGE_QUALITY_BILINEAR``, ``wx.IMAGE_QUALITY_BICUBIC``,
         ``wx.IMAGE_QUALITY_BOX_AVERAGE``, ``wx.IMAGE_QUALITY_NORMAL``,
         ``wx.IMAGE_QUALITY_HIGH``
        """
        self.imageQuality = imageQuality

    def GetUseBackgroundTexture(self):
        """
        Get whether the use background texture option is set.

        :rtype: bool
        """
        return self.useBackgroundTexture

    def SetUseBackgroundTexture(self, useBackgroundTexture):
        """
        Set whether to use background texture option.

        :type `useBackgroundTexture`: bool
        """
        self.useBackgroundTexture = useBackgroundTexture
        self.OnSize()

    def ToggleUseBackgroundTexture(self, event=None):
        """
        Toggle the use a background texture option.
        """
        self.useBackgroundTexture = not self.useBackgroundTexture
        self.OnSize()

    def SetAllowOverscaling(self, allowOverscaling):
        """
        Set whether the image should be overscaled if the panel's size is
        bigger than the picture's size.

        :param `allowOverscaling`: Set whether the picture should be overscaled.
        :type `allowOverscaling`: bool
        """
        self.allowOverscaling = allowOverscaling

    def SetAllowDownscaling(self, allowDownscaling):
        """
        Set whether the image should be downscaled if the panel's size is
        smaller than the picture's size.

        :param `allowDownscaling`: Set whether the picture should be overscaled.
        :type `allowDownscaling`: bool
        """
        self.allowDownscaling = allowDownscaling

    def GetPictureBackgroundColor(self):
        """
        Get the color to display for the picture's background.

        :returns: A `wx.Colour`
        """
        if isinstance(self.backgroundColor, wx.Colour):
            return self.backgroundColor
        elif isinstance(self.backgroundColor, wx.Brush):
            return self.backgroundColor.GetColour()

    def SetPictureBackgroundColor(self, backgroundColor):
        """
        Set the color to display for the picture's background.

        :param `backgroundColor`: The color to display for the picture's background.
        :type `backgroundColor`: A `wx.Colour` or (int(r), int(g), int(b)) tuple
        """
        if isinstance(backgroundColor, tuple):
            backgroundColor = wx.Colour(backgroundColor)
        if isinstance(backgroundColor, wx.Colour):
            backgroundColor = wx.Brush(backgroundColor)
        self.backgroundColor = backgroundColor
        self.OnSize()

    def SetPicture(self, picture):
        """
        Set the picture's bitmap.

        :param `picture`: The bitmap to display.
        :type `picture`: A `wx.Bitmap`
        """
        if isinstance(picture, wx.Bitmap):
            self.origbitmap = picture
            self.bitmap = picture
        else:  # Figure out if we can use what was sent in other ways.
            self.origbitmap = self._ConvertifyToPicture(picture)
            self.bitmap = self._ConvertifyToPicture(picture)
        self.OnSize()

    def OnSize(self, event=None):
        """
        Handles the ``wx.EVT_SIZE`` event for :class:`Picture`.

        :param `event`: A `wx.SizeEvent` to be processed.
        :type `event`: `wx.SizeEvent`
        """
        winX = self.Size[0]
        winY = self.Size[1]
        if winX <= 0 or winY <= 0:
            return
        self.buffer = wx.Bitmap(winX, winY)
        dc = wx.MemoryDC()
        dc.SelectObject(self.buffer)
        dc.SetBackground(self.backgroundColor)
        dc.Clear()
        if self.useBackgroundTexture and self.backgroundTextureBmp:
            stippleBrush = wx.Brush()
            stippleBrush.SetStyle(wx.BRUSHSTYLE_STIPPLE_MASK)
            stippleBrush.SetStipple(self.backgroundTextureBmp)
            dc.SetBrush(stippleBrush)  # STIPPLE Background
            dc.DrawRectangle(0, 0, winX, winY)  # STIPPLE Background
        if self.bitmap:
            bmpX, bmpY = self.bitmap.GetSize()

            scale = min(float(winX) / bmpX, float(winY) / bmpY)
            bmpX_Scaled = int(bmpX * scale)
            bmpY_Scaled = int(bmpY * scale)
            if bmpX_Scaled <= 0 or bmpY_Scaled <= 0:
                return
            if not self.allowOverscaling and not self.allowDownscaling:
                dc.DrawBitmap(self.bitmap,
                              winX / 2 - bmpX / 2,
                              winY / 2 - bmpY / 2)
            elif self.allowOverscaling and self.allowDownscaling:
                dc.DrawBitmap(wx.Bitmap(self.bitmap.ConvertToImage().
                                Rescale(bmpX_Scaled, bmpY_Scaled, self.imageQuality)),
                              max(0, winX - bmpX_Scaled) / 2,
                              max(0, winY - bmpY_Scaled) / 2)
            elif self.allowDownscaling:
                if winX <= bmpX or winY <= bmpY:
                    dc.DrawBitmap(wx.Bitmap(self.bitmap.ConvertToImage().
                                    Rescale(bmpX_Scaled, bmpY_Scaled, self.imageQuality)),
                                  max(0, winX - bmpX_Scaled) / 2,
                                  max(0, winY - bmpY_Scaled) / 2)
                else:
                    dc.DrawBitmap(self.bitmap,
                                  winX / 2 - bmpX / 2,
                                  winY / 2 - bmpY / 2)
            elif self.allowOverscaling:
                if winX >= bmpX and winY >= bmpY:
                    dc.DrawBitmap(wx.Bitmap(self.bitmap.ConvertToImage().
                                    Rescale(bmpX_Scaled, bmpY_Scaled, self.imageQuality)),
                                  max(0, winX - bmpX_Scaled) / 2,
                                  max(0, winY - bmpY_Scaled) / 2)
                else:  # Squeeze imgWidth x imgHeight image into window, preserving the aspect ratio.
                    xFactor = float(winX) / bmpX
                    yFactor = float(winY) / bmpY

                    if xFactor < 1.0 and xFactor < yFactor:
                        scale = xFactor
                    elif yFactor < 1.0 and yFactor < xFactor:
                        scale = yFactor
                    else:
                        scale = 1.0
                    bmpX_Scaled = int(bmpX * scale)
                    bmpY_Scaled = int(bmpY * scale)

                    dc.DrawBitmap(self.bitmap,
                                  winX / 2 - bmpX / 2,
                                  winY / 2 - bmpY / 2)
        del dc
        self.Refresh()
        self.Update()

    def OnEraseBackground(self, event):
        """
        Handles the ``wx.EVT_ERASE_BACKGROUND`` event for :class:`Picture`.

        :param `event`: A `wx.EraseEvent` to be processed.
        :type `event`: `wx.EraseEvent`
        """
        pass  # Reduce flicker with buffered paint

    def OnPaint(self, event):
        """
        Handles the ``wx.EVT_PAINT`` event for :class:`Picture`.

        :param `event`: A `wx.PaintEvent` to be processed.
        :type `event`: `wx.PaintEvent`
        """
        dc = wx.BufferedPaintDC(self, self.buffer)

    def _ConvertifyToPicture(self, wtf):
        """
        See if the object argument passed is covertable to bitmap
        for use with :class:`Picture`.

        :returns: A `wx.Bitmap` or raises an Exception.
        """
        if isinstance(wtf, wx.Image):
            wtf = wtf.ConvertToBitmap()
            return wtf
        elif isinstance(wtf, wx.Icon):
            width = wtf.GetWidth()
            height = wtf.GetHeight()
            bmp = wx.Bitmap(width, height)
            bmp.CopyFromIcon(wtf)
            return bmp
        elif isinstance(wtf, str):  # Might be a filepath...
            if Picture.IsMyImageFileSupported(wtf):
                return wx.Bitmap(wtf)
        else:
            raise Exception('Unknown supported picture type.\n%s' % wtf)

    @staticmethod
    def IsMyImageFileSupported(filepath):
        import os
        ext = os.path.splitext(filepath)[1]  # Get the file extension.
        # Check if image type is supported.
        return ext.lower() in wx.Image.GetImageExtWildcard()


if __name__ == '__main__':
    # Sample App.
    import os
    import sys
    def GetSnakeyBmpMemoryDC(bmpScale=0):
        """
        Draw Metallicow's favorite little mascot, Snakey :)~

        :param `bmpScale`: Scale snaky bigger than (16, 16) pixels default.
        :type `bmpScale`: int or float
        :returns: A `wx.Bitmap`
        """
        bmp = wx.Bitmap(16, 16)
        dc = wx.MemoryDC(bmp)
        dc.SetBrush(wx.TRANSPARENT_BRUSH)
        dc.SetPen(wx.TRANSPARENT_PEN)
        dc.SetBackgroundMode(wx.TRANSPARENT)
        dc.Clear()
        dc.DrawRectangle(wx.Rect(0, 0, 16, 16))

        # Draw the Skin.
        dc.GradientFillLinear(wx.Rect(2, 2, 13, 13), '#15FF19', '#DBFFDB')
        # Draw Outline.
        dc.SetPen(wx.BLACK_PEN)
        dc.DrawLineList(lines=((1, 1, 15, 1), (11, 2, 13, 2), (14, 2, 15, 2),
            (3, 4, 15, 4), (1, 6, 13, 6), (3, 8, 15, 8), (1, 10, 13, 10),
            (3, 12, 15, 12), (1, 1, 1, 14), (1, 14, 15, 14), (1, 1, 14, 1),
            (14, 4, 14, 14)), pens=None)
        # Draw the Tongue :)~
        dc.SetPen(wx.RED_PEN)
        dc.DrawPointList(points=((14, 3), (15, 3), (15, 4)), pens=None)

        if bmpScale:
            img = dc.GetAsBitmap().ConvertToImage()
            img = img.Rescale(16 * bmpScale, 16 * bmpScale,
                              wx.IMAGE_QUALITY_NEAREST)
            img.SetMaskColour(255, 255, 254)  # Not quite white.
            bmp = img.ConvertToBitmap()
            return bmp

        return dc.GetAsBitmap()

    class MyFrame(wx.Frame):
        def __init__(self, parent, id=wx.ID_ANY, title=_(u"Picture Demo"),
                     pos=wx.DefaultPosition):
            wx.Frame.__init__(self, parent, id, title, pos)
            # pass an image on the commandline or drop an image on file.
            if len(sys.argv) > 1:
                arg = sys.argv[1]
                if os.path.exists(arg):  # Check if it exists.
                    if os.path.isfile(arg):  # Must be a file.
                        ext = os.path.splitext(arg)[1]  # Get the file extension.
                        # Check if image type is supported.
                        if Picture.IsMyImageFileSupported(arg):
                            self.pic = pic = Picture(self, picture=wx.Bitmap(arg),
                                          imageQuality=wx.IMAGE_QUALITY_HIGH)
                            pic.SetAllowOverscaling(True)
            else:  # Just use Snakey!
                self.pic = pic = Picture(self,
                              imageQuality=wx.IMAGE_QUALITY_NEAREST,
                              backgroundColor=wx.WHITE,
                              backgroundTextureBmp=GetSnakeyBmpMemoryDC()
                              )
                pic.SetPicture(GetSnakeyBmpMemoryDC(bmpScale=10))
                pic.SetAllowOverscaling(False)  # Testing mouse scaling
                pic.SetAllowDownscaling(False)  # Testing mouse scaling
                pic.ToggleUseBackgroundTexture()
                pic.Bind(wx.EVT_LEFT_DCLICK, pic.ToggleUseBackgroundTexture)
                tt1 = _(u'Right click on the picture to show the built-in popup menu with options.')
                tt2 = _(u'Resize the frame to scale the picture.')
                tt = '\n'.join((tt1, tt2))
                pic.SetToolTip(wx.ToolTip(tt))

            self.CreateStatusBar().SetStatusText('wxPython %s' % wx.version())

    # our normal wxApp-derived class, as usual

    app = wx.App(0)

    frame = MyFrame(None, pos=(20, 20))
    app.SetTopWindow(frame)
    frame.Show()

    app.MainLoop()

