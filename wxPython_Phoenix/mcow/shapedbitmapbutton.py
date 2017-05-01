#!/usr/bin/env python


# --------------------------------------------------------------------------- #
# SHAPEDBITMAPBUTTON Control wxPython IMPLEMENTATION
# Python Code By:
#
# Edward Greig, @ 17 Jan 2014
# Latest Revision: Edward Greig 24 Nov 2015, 21.00 GMT
#
#
# TODO List/Caveats
#
# 1. Creating *A Lot* Of ShapedBitmapButtons May Require Some Time.
#
#
# For All Kind Of Problems, Requests Of Enhancements And Bug Reports, Please
# Write To Me At:
#
# metaliobovinus@gmail.com
#
# Or, Obviously, To The wxPython Mailing List!!!
#
#
# End Of Comments
# --------------------------------------------------------------------------- #


"""
ShapedBitmapButton
==================

`ShapedBitmapButton` tries to fill the lack of "custom shaped" controls in wxPython
and it can be used to build round or custom-shaped buttons from images with
alpha(PNG).


Description
-----------

`ShapedBitmapButton` tries to fill the lack of "custom shaped" controls in wxPython
(that depends on the same lack in wxWidgets). It can be used to build round
buttons or elliptic buttons.

`ShapedBitmapButton` is based on a :class:`Window`, in which multiple images are
drawn depending on the button state (pressed, not pressed, hovering, disabled).

`ShapedBitmapButton` has the ability to draw it's parent widgets background
colour or tiled bitmap, so that everything looks nice.

`ShapedBitmapButton` reacts on mouse events *only* if the mouse event occurred inside
the image region, even if `ShapedBitmapButton` is built on a rectangular window.


Usage
-----

Usage example::

    import wx
    import wx.lib.mcow.shapedbitmapbutton as SBB

    class MyFrame(wx.Frame):
        def __init__(self, parent):
            wx.Frame.__init__(self, parent, -1, "ShapedBitmapButton Demo")

            # Optionally define a bitmap to use for the Paint Event Handler and
            # the ShapedBitmapButtons parentBgBmp keywordArg.
            bmp = wx.Bitmap('seamless.png', wx.BITMAP_TYPE_PNG)
            self.backgroundBitmap = SBB.ShapedBitmapButton.MakeDisplaySizeBackgroundBitmap(bmp)

            # Create 1-5 bitmaps for the button. bitmap is required.
            sButton = SBB.ShapedBitmapButton(self, -1,
                bitmap=wx.Bitmap('shapedbitmapbutton-normal.png', wx.BITMAP_TYPE_PNG),
                pressedBmp=wx.Bitmap('shapedbitmapbutton-pressed.png', wx.BITMAP_TYPE_PNG),
                hoverBmp=wx.Bitmap('shapedbitmapbutton-hover.png', wx.BITMAP_TYPE_PNG),
                disabledBmp=wx.Bitmap('shapedbitmapbutton-disabled.png', wx.BITMAP_TYPE_PNG),
                parentBgBmp=self.backgroundBitmap,
                pos=(20, 20))
            sButton.Bind(wx.EVT_BUTTON, self.OnButton)

            # Optionally Add these for the custom background painting.
            self.Bind(wx.EVT_PAINT, self.OnPaint)
            self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)

        def OnButton(self, event):
            print('wxPython Rocks!')

        def OnEraseBackground(self, event):
            pass

        def OnPaint(self, event):
            dc = wx.BufferedPaintDC(self)
            dc.Clear()
            dc.DrawBitmap(self.backgroundBitmap, 0, 0, True)

    # our normal wxApp-derived class, as usual

    app = wx.App(0)

    frame = MyFrame(None)
    app.SetTopWindow(frame)
    frame.Show()

    app.MainLoop()


Methods and Settings
--------------------

With `ShapedBitmapButton` you can:

- Create rounded/elliptical buttons/togglebuttons;
- Set images for the enabled/disabled/focused/selected state of the button;
- Set an background image (will be tiled-seamless textures work best) for the button;
- Create other great looking custom widgets(Ex: Notebook Tabs, Personas, Graphical Grids/Tables)
  fast and easily with images containing alpha;
- Create point and click games/apps;
- Never worry about the calculating the custom shape of your buttons again;
- Improve the look and functionality of current basic buttons in applications;

TODO Methods:

- Draw the focus indicator (or disable it);
- Draw the focus indicator and label with(Option for Adjustable Blur/DropShadows);
- Set label colour and font(LabelEnable);
- Apply a rotation/pos to the `ShapedBitmapButton` label;
- Change `ShapedBitmapButton` size and text orientation in runtime.(Ex: SVG);
- Integrate CheckBox Functionalities so a 3-way/multiple way CustomCheckbox is possible.


Window Styles
-------------

`No particular window styles are available for this class.`


Events Processing
-----------------

This class processes the following events:

================= ==================================================
Event Name        Description
================= ==================================================
``wx.EVT_BUTTON`` Process a `wxEVT_COMMAND_BUTTON_CLICKED` event, when the button is clicked.
================= ==================================================


Supported Platforms
-------------------
:class:`ShapedBitmapButton` has been tested on the following platforms:
  * Windows (Windows XP, 7).


License And Version
-------------------

`ShapedBitmapButton` is distributed under the wxPython license.

Edward Greig, @ 17 Jan 2014
Latest revision: Edward Greig @ 24 Nov 2015, 21.00 GMT

Version 0.3.2

"""




##  import time # DEBUGGING

import wx
from wx import GetMousePosition as wxGetMousePosition

## print(wx.version())
PHOENIX = 'phoenix' in wx.version()
if PHOENIX:
    # Classic Vs.Phoenix Compatibility/Deprecations.
    wx.RegionFromBitmapColour = wx.Region
    wx.PyCommandEvent = wx.CommandEvent
    wx.PyControl = wx.Control
    wx.EmptyBitmap = wx.Bitmap
    wx.BrushFromBitmap = wx.Brush


HOVER = 1
""" Flag used to indicate that the mouse is hovering on a :class:`ShapedBitmapButton`. """
CLICK = 2
""" Flag used to indicate that the :class:`ShapedBitmapButton` is on a pressed state. """


def MakeDisplayWidthBackgroundBitmap(bitmap=wx.NullBitmap):
    """
    Makes and returns a display width size(fullscreen width x bitmap height) bitmap
    to tile seamlessly for the :class:`ShapedBitmapButton`'s parent.
    This should be the same visually as for, example the parent widget's
    Paint handler would produce.

    :param `bitmap`: the bitmap to be tiled, an instance of :class:`Bitmap`.
    :returns: a display width size bitmap to be tiled, an instance of :class:`Bitmap`.
    :rtype: :class:`Bitmap`
    """
    if not bitmap:
        raise Exception('Need a Bitmap!')  # TODO Make Custom Exception Class??? MissingBitmapError...
    bmpW = bitmap.GetWidth()
    bmpH = bitmap.GetHeight()
    if not bmpW or not bmpH:
        raise Exception('Bitmap width and height should be greater than 0!')
    width, height = wx.GetDisplaySize()
    bmp = wx.EmptyBitmap(width, bmpH)
    mdc = wx.MemoryDC(bmp)

    bmpBrush = wx.BrushFromBitmap(bitmap)
    mdc.SetBrush(bmpBrush)
    mdc.DrawRectangle(-1, -1, width + 2, bmpH + 2)
    # ...or this would work too. timeit: BrushFromBitmap way is faster.
    ## localDrawBitmap = mdc.DrawBitmap
    ## [localDrawBitmap(bitmap, x, 0, True)
    ##     for x in range(0, width, bmpW)]

    return mdc.GetAsBitmap(wx.Rect(0, 0, width, bmpH))


def MakeDisplayHeightBackgroundBitmap(bitmap=wx.NullBitmap):
    """
    Makes and returns a display height size(bitmap width x fullscreen height) bitmap
    to tile seamlessly for the :class:`ShapedBitmapButton`'s parent.
    This should be the same visually as for, example the parent widget's
    Paint handler would produce.

    :param `bitmap`: the bitmap to be tiled, an instance of :class:`Bitmap`.
    :returns: a display height size bitmap to be tiled, an instance of :class:`Bitmap`.
    :rtype: :class:`Bitmap`
    """
    if not bitmap:
        raise Exception('Need a Bitmap!')  # TODO Make Custom Exception Class??? MissingBitmapError...
    bmpW = bitmap.GetWidth()
    bmpH = bitmap.GetHeight()
    if not bmpW or not bmpH:
        raise Exception('Bitmap width and height should be greater than 0!')
    width, height = wx.GetDisplaySize()
    bmp = wx.EmptyBitmap(bmpW, height)
    mdc = wx.MemoryDC(bmp)

    bmpBrush = wx.BrushFromBitmap(bitmap)
    mdc.SetBrush(bmpBrush)
    mdc.DrawRectangle(-1, -1, bmpW + 2, height + 2)
    # ...or this would work too. timeit: BrushFromBitmap way is faster.
    ## localDrawBitmap = mdc.DrawBitmap
    ## [localDrawBitmap(bitmap, 0, y, True)
    ##     for y in range(0, height, bmpH)]

    return mdc.GetAsBitmap(wx.Rect(0, 0, bmpW, height))


def MakeDisplaySizeBackgroundBitmap(bitmap=wx.NullBitmap):
    """
    Makes and returns a display size(fullscreen width x height) bitmap
    to tile seamlessly for the :class:`ShapedBitmapButton`'s parent.
    This should be the same visually as for, example the parent widget's
    Paint handler would produce.

    :param `bitmap`: the bitmap to be tiled, an instance of :class:`Bitmap`.
    :returns: a display size bitmap to be tiled, an instance of :class:`Bitmap`.
    :rtype: :class:`Bitmap`
    """
    if not bitmap:
        raise Exception('Need a Bitmap!')  # TODO Make Custom Exception Class??? MissingBitmapError...
    bmpW = bitmap.GetWidth()
    bmpH = bitmap.GetHeight()
    if not bmpW or not bmpH:
        raise Exception('Bitmap width and height should be greater than 0!')
    width, height = wx.GetDisplaySize()
    bmp = wx.EmptyBitmap(width, height)
    mdc = wx.MemoryDC(bmp)

    bmpBrush = wx.BrushFromBitmap(bitmap)
    mdc.SetBrush(bmpBrush)
    mdc.DrawRectangle(-1, -1, width + 2, height + 2)
    # ...or this would work too. timeit: BrushFromBitmap way is faster.
    ## localDrawBitmap = mdc.DrawBitmap
    ## [[localDrawBitmap(bitmap, x, y, True)
    ##     for y in range(0, height, bmpH)]
    ##         for x in range(0, width, bmpW)]

    return mdc.GetAsBitmap(wx.Rect(0, 0, width, height))


class ShapedBitmapButtonEvent(wx.PyCommandEvent):
    """ Event sent from :class:`ShapedBitmapButton` when the button is activated. """

    def __init__(self, eventType, eventId):
        """
        Default class constructor.

        :param `eventType`: the event type;
        :param `eventId`: the event identifier.
        """

        wx.PyCommandEvent.__init__(self, eventType, eventId)
        self.isDown = False
        self.theButton = None

    def SetIsDown(self, isDown):
        """
        Sets the button event as pressed.

        :param `isDown`: ``True`` to set the event as "pressed", ``False`` otherwise.
        """

        self.isDown = isDown

    def GetIsDown(self):
        """ Returns ``True`` if the button event is "pressed". """

        return self.isDown

    def SetButtonObj(self, btn):
        """
        Sets the event object for the event.

        :param `btn`: the button object, an instance of :class:`ShapedBitmapButton`.
        """

        self.theButton = btn

    def GetButtonObj(self):
        """
        Returns the object associated with this event.

        :return: An instance of :class:`ShapedBitmapButton`.
        """

        return self.theButton


class ShapedBitmapButton(wx.PyControl):
    """ This is the main class implementation of :class:`ShapedBitmapButton`. """
    def __init__(self, parent, id=wx.ID_ANY, bitmap=wx.NullBitmap,
                 pressedBmp=None, hoverBmp=None, disabledBmp=None, parentBgBmp=None,
                 label="", labelEnable=True, labelForeColour=wx.BLACK, labelBackColour=wx.TransparentColour,
                 labelStrokeColour=wx.WHITE,
                 labelStrokeWidth=0, labelDropShadowBlur=3, labelDropShadowDist=3,
                 labelFont=None, labelPosition=(0, 0), labelRotation=0.0,
                 raiseOnSetFocus=True,
                 pos=wx.DefaultPosition, size=wx.DefaultSize,
                 style=wx.NO_BORDER, validator=wx.DefaultValidator,
                 name="shapedbutton"):
        """
        Default class constructor.

        :param `parent`: the :class:`ShapedBitmapButton` parent;
        :param `id`: window identifier. A value of -1 indicates a default value;
        :param `bitmap`: the button bitmap (if any);
        :param `pressedBmp`: the pressed button bitmap (if any);
        :param `hoverBmp`: the hover button bitmap (if any);
        :param `disabledBmp`: the disabled button bitmap (if any);
        :param `label`: the button text label;
        :param `labelEnable`: draw the label?;
        :param `labelForeColour`: the label foreground colour;
        :param `labelBackColour`: the label background colour;
        :param `labelBackgroundMode`: ``wx.TRANSPARENT``(default) or ``wx.SOLID``;
        :param `pos`: the control position. A value of (-1, -1) indicates a default position,
         chosen by either the windowing system or wxPython, depending on platform;
        :param `size`: the control size. A value of (-1, -1) indicates a default size,
         chosen by either the windowing system or wxPython, depending on platform;
        :param `style`: the button style (unused);
        :param `validator`: the validator associated to the button;
        :param `name`: the button name.
        """

        wx.PyControl.__init__(self, parent, id, pos, size, style, validator, name)

        self.parent = parent

        self._bitmap = bitmap
        ## if not bitmap.GetWidth() and not bitmap.GetHeight(): # wx.NullBitmap
        ##     self._bitmap = wx.Bitmap(1, 1)

        self._pressedBmp = pressedBmp
        self._hoverBmp = hoverBmp
        try:
            self._disabledBmp = disabledBmp or bitmap.ConvertToDisabled()
        except AttributeError:
            self._disabledBmp = disabledBmp or \
                bitmap.ConvertToImage().ConvertToGreyscale().ConvertToBitmap()

        self._regionColour = wx.TransparentColour  # wx.Colour(0, 0, 0, 0)  # Alpha
        self._region = wx.RegionFromBitmapColour(bitmap, self._regionColour)

        self._parentBgBmp = parentBgBmp

        self._raiseOnSetFocus = raiseOnSetFocus
        self._makeChildBmp = False  # Used by ShapedBitmapButton children
        self._sbbChildBmp = None    # Used by ShapedBitmapButton children

        self._mouseAction = None
        # self._hasFocus = False
        self._mouseIsInRegion = False
        # Label attributes.
        self._label = label
        self._labelsList = []
        self._labelEnable = labelEnable
        self._labelBackColour = labelBackColour
        self._labelForeColour = labelForeColour
        self._labelStrokeColour = labelStrokeColour
        self._labelStrokeWidth = labelStrokeWidth
        self._labelDropShadowBlur = labelDropShadowBlur
        self._labelDropShadowDist = labelDropShadowDist
        self._labelPosition = labelPosition
        self._labelRotation = float(labelRotation)
        self._labelFont = wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT) if not labelFont else labelFont

        self_Bind = self.Bind
        self_Bind(wx.EVT_SIZE, self.OnSize)
        self_Bind(wx.EVT_PAINT, self.OnPaint)
        self_Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        self_Bind(wx.EVT_LEFT_DCLICK, self.OnLeftDClick)
        self_Bind(wx.EVT_LEFT_UP, self.OnLeftUp)
        self_Bind(wx.EVT_RIGHT_DOWN, self.OnRightDown)
        self_Bind(wx.EVT_RIGHT_DCLICK, self.OnRightDClick)
        self_Bind(wx.EVT_RIGHT_UP, self.OnRightUp)
        self_Bind(wx.EVT_MIDDLE_DOWN, self.OnMiddleDown)
        self_Bind(wx.EVT_MIDDLE_DCLICK, self.OnMiddleDClick)
        self_Bind(wx.EVT_MIDDLE_UP, self.OnMiddleUp)
        self_Bind(wx.EVT_MOUSE_AUX1_DOWN, self.OnAux1Down)
        self_Bind(wx.EVT_MOUSE_AUX1_UP, self.OnAux1Up)
        self_Bind(wx.EVT_MOUSE_AUX1_DCLICK, self.OnAux1DClick)
        self_Bind(wx.EVT_MOUSE_AUX2_DOWN, self.OnAux2Down)
        self_Bind(wx.EVT_MOUSE_AUX2_UP, self.OnAux2Up)
        self_Bind(wx.EVT_MOUSE_AUX2_DCLICK, self.OnAux2DClick)
        self_Bind(wx.EVT_MOTION, self.OnMotion)
        self_Bind(wx.EVT_LEAVE_WINDOW, self.OnLeaveWindow)
        self_Bind(wx.EVT_ENTER_WINDOW, self.OnEnterWindow)
        self_Bind(wx.EVT_MOUSEWHEEL, self.OnMouseWheel)
        # self_Bind(wx.EVT_MOUSE_EVENTS, self.OnMouseEvents)
        self_Bind(wx.EVT_CONTEXT_MENU, self.OnContextMenu)
        self_Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)
        self_Bind(wx.EVT_KEY_UP, self.OnKeyUp)
        self_Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)
        # self_Bind(wx.EVT_SET_FOCUS, self.OnGainFocus)
        # self_Bind(wx.EVT_KILL_FOCUS, self.OnLoseFocus)

        self.SetLabel(label)
        self.InheritAttributes()
        self.SetInitialSize(size)

        self.SetBackgroundStyle(wx.BG_STYLE_PAINT)

        imAChild = hasattr(self.GetParent(), '_sbbChildBmp')
        if imAChild:  # I am a child here.
            wx.CallAfter(self.parent.MakeChildBmp)
            wx.CallAfter(self.Refresh)


    def UpdateBackgroundColourFromParent(self):
        self.SetBackgroundColour(self.parent.GetBackgroundColour())
        self.Refresh()

    def Rotate180(self):
        """
        Rotates the button bitmaps by 180 degrees.
        """
        self._bitmap = self._bitmap.ConvertToImage().Rotate180().ConvertToBitmap()
        self._pressedBmp = self._pressedBmp.ConvertToImage().Rotate180().ConvertToBitmap()
        self._hoverBmp = self._hoverBmp.ConvertToImage().Rotate180().ConvertToBitmap()
        self._disabledBmp = self._disabledBmp.ConvertToImage().Rotate180().ConvertToBitmap()
        self._region = wx.RegionFromBitmapColour(self._bitmap, self._regionColour)

    def Rotate90(self, clockwise=True):
        """
        Rotates the button bitmaps 90 degrees in the direction indicated by ``clockwise``.

        :param `clockwise`: ``True`` for horizontally and ``False`` for vertically.
        :type `clockwise`: bool
        """

        self._bitmap = self._bitmap.ConvertToImage().Rotate90(clockwise).ConvertToBitmap()
        self._pressedBmp = self._pressedBmp.ConvertToImage().Rotate90(clockwise).ConvertToBitmap()
        self._hoverBmp = self._hoverBmp.ConvertToImage().Rotate90(clockwise).ConvertToBitmap()
        self._disabledBmp = self._disabledBmp.ConvertToImage().Rotate90(clockwise).ConvertToBitmap()
        self._region = wx.RegionFromBitmapColour(self._bitmap, self._regionColour)

    def Mirror(self, horizontally=True):
        """
        Mirrors the button. The parameter ``horizontally`` indicates the orientation.

        :param `horizontally`: ``True`` for horizontally and ``False`` for vertically.
        :type `horizontally`: bool
        """
        self._bitmap = self._bitmap.ConvertToImage().Mirror(horizontally).ConvertToBitmap()
        self._pressedBmp = self._pressedBmp.ConvertToImage().Mirror(horizontally).ConvertToBitmap()
        self._hoverBmp = self._hoverBmp.ConvertToImage().Mirror(horizontally).ConvertToBitmap()
        self._disabledBmp = self._disabledBmp.ConvertToImage().Mirror(horizontally).ConvertToBitmap()
        self._region = wx.RegionFromBitmapColour(self._bitmap, self._regionColour)

    def GetBackgroundBitmap(self):
        return self._parentBgBmp

    def SetBackgroundBitmap(self, bitmap):
        self._parentBgBmp = bitmap

    @staticmethod
    def WillLabelTextFitInsideButton(bitmap, text, font=None):
        """
        Will the text(unrotated) fit inside the buttons rectangle.

        :param `bitmap`: the bitmap for the button
        :type `bitmap`: `wx.Bitmap`
        :param `text`: text to measure
        :type `text`: str
        :param `font`: font for the text
        :type `font`: `wx.Font`
        """
        sdc = wx.ScreenDC()
        if PHOENIX:
            width, height, lineHeight = sdc.GetFullMultiLineTextExtent(text, font)
        else:
            width, height, lineHeight = sdc.GetMultiLineTextExtent(text, font)
        bmpW = bitmap.GetWidth()
        bmpH = bitmap.GetHeight()
        return width < bmpW and height < bmpH

    def GetLabel(self):
        """
        Get the buttons text label.

        :returns: The buttons text label to be drawn.
        :rtype: str
        """
        return self._label

    def SetLabel(self, label=None):
        """
        Set the buttons text label.

        :param `label`: The buttons text label to be drawn.
        :type `label`: str
        """
        if label is None:
            label = ''
        self._label = label

    def GetLabelsList(self):
        """
        Get the buttons text labels list.

        :returns: The list of [labels, coords, foregrounds, backgrounds] to be drawn.
        :rtype: list
        """
        return self._labelsList

    def SetLabelsList(self, labelsList=[], coords=[], foregrounds=[], backgrounds=[], fonts=[], rotations=[]):
        """
        Set the buttons text labels list.

        :param `labelsList`: A list of text labels to be drawn.
        :type `labelsList`: list
        :param `coords`: A list of (x,y) positions. List length must be equal to the length of labelsList.
        :type `coords`: list
        :param `foregrounds`: A list of wx.Colour objects to use for the foregrounds of the strings. If nothing is passed, use the default colour in the constructor.
        :type `foregrounds`: list of wx.Colours or a single wx.Colour
        :param `backgrounds`: A list of wx.Colour objects to use for the backgrounds of the strings. If nothing is passed, use the default colour in the constructor.
         Note: ``wx.TransparentColour`` is a valid colour for the text backgrounds.
        :type `backgrounds`: list of wx.Colours or a single wx.Colour
        :param `fonts`: A list of wx.Font objects to use for the fonts of the strings. If nothing is passed, use the default font in the constructor.
        :type `fonts`: list of fonts or a single wx.Font
        :param `rotations`: A list of floats to use for the rotations of the strings. If nothing is passed, use the default rotation in the constructor.
        :type `rotations`: list of floats or a single float
        """
        if not labelsList:
            self._labelsList = labelsList
            return
        assert len(labelsList) == len(coords) # == len(foregrounds) == len(backgrounds) == len(fonts) == len(rotations)
        if not foregrounds:
            fg = self._labelForeColour
            foregrounds = [fg] * len(labelsList)
        elif isinstance(foregrounds, wx.Colour):
            foregrounds = [foregrounds] * len(labelsList)
        if not backgrounds:
            bg = self._labelBackColour
            backgrounds = [bg] * len(labelsList)
        elif isinstance(backgrounds, wx.Colour):
            backgrounds = [backgrounds] * len(labelsList)
        if not fonts:
            fnt = self._labelFont
            fonts = [fnt] * len(labelsList)
        elif isinstance(fonts, wx.Font):
            fonts = [fonts] * len(labelsList)
        if not rotations:
            rot = self._labelRotation
            rotations = [rot] * len(labelsList)
        elif isinstance(rotations, (int, float)):
            rotations = [rotations] * len(labelsList)
        rotations = [float(rot) for rot in rotations]

        self._labelsList = zip(labelsList, coords, foregrounds, backgrounds, fonts, rotations)

    def GetLabelEnabled(self):
        """
        :returns: ``True`` if the button's label is enabled, ``False`` otherwise.
        :rtype: bool
        """
        return self._labelEnable

    def SetLabelEnabled(self, enable=True):
        """
        Set whether the label should be drawn for :class:`ShapedBitmapButton`.

        :param `enable`: ``True`` to enable drawing the button's label, ``False`` to disable it.
        :type `enable`: bool
        """
        self._labelEnable = enable

    def GetLabelColour(self):
        """
        Get the button label colour.

        :returns: the button label colour.
        :rtype: `wx.Colour`
        """

        return self._labelForeColour

    def SetLabelColour(self, colour=None):
        """
        Sets the button label colour.

        :param `colour`: an instance of :class:`Colour`.
        """

        if colour is None:
            colour = wx.BLACK

        self._labelForeColour = colour

    def SetLabelRotation(self, angle=None):
        """
        Sets angle of button label rotation.

        :param `angle`: the label rotation, in degrees.
        :type `angle`: float
        """

        if angle is None:
            angle = 0

        self._labelRotation = float(angle)

    def SetLabelPosition(self, pos=None):
        """
        Sets the position of button label.

        :param `pos`: the label position.
        :type `pos`: point
        """

        if pos is None:
            pos = (0, 0)

        self._labelPosition = pos

    def OnEraseBackground(self, event):
        """
        Handles the ``wx.EVT_ERASE_BACKGROUND`` event for :class:`ShapedBitmapButton`.

        :param `event`: a :class:`EraseEvent` event to be processed.
        """

        # This is intentionally empty, because we are using the combination
        # of wx.BufferedPaintDC + an empty OnEraseBackground event to
        # reduce flicker
        pass

    def DoGetBestSize(self):

        return self._bitmap.GetSize()

    def AcceptsFocus(self):
        """
        Can this window be given focus by mouse click?

        :note: Overridden from `wx.PyControl`.
        """

        return self.IsShown() and self.IsEnabled()

    def Enable(self, enable=True):
        """
        Enables/disables the button.

        :param `enable`: ``True`` to enable the button, ``False`` to disable it.

        :note: Overridden from :class:`PyControl`.
        """

        wx.PyControl.Enable(self, enable)
        self.Refresh()

    def OnSize(self, event):
        """
        Handles the ``wx.EVT_SIZE`` event for :class:`ShapedBitmapButton`.

        :param `event`: a :class:`SizeEvent` event to be processed.
        """
        self.Refresh()
        event.Skip()
        # print('OnSize')

    def SetParentBackgroundBitmap(self, bitmap):
        """
        Sets the bitmap to tile seamlessly for the :class:`ShapedBitmapButton`'s parent.
        This should be the same visually as for, example the parent widget's
        Paint handler would produce.

        :param `bitmap`: the bitmap to set, an instance of :class:`Bitmap`.
        """
        self._parentBgBmp = bitmap

    def GetBitmap(self):
        """
        Gets the bitmap for the :class:`ShapedBitmapButton`.

        :returns: the bitmap
        :rtype: `wx.Bitmap`
        """

        return self._bitmap

    def SetBitmap(self, bitmap):
        """
        Sets the bitmap for the :class:`ShapedBitmapButton`.

        :param `bitmap`: the bitmap to set, an instance of :class:`Bitmap`.
        """

        self._bitmap = bitmap
        self.Refresh()

    def GetBitmapPressed(self):
        """
        Gets the pressed bitmap for the :class:`ShapedBitmapButton`.

        :returns: the pressed bitmap
        :rtype: `wx.Bitmap`
        """

        return self._pressedBmp

    def SetBitmapPressed(self, bitmap):
        """
        Sets the pressed bitmap for the :class:`ShapedBitmapButton`.

        :param `bitmap`: the pressed bitmap to set, an instance of :class:`Bitmap`.
        """

        self._pressedBmp = bitmap
        self.Refresh()

    def GetBitmapHover(self):
        """
        Gets the hover bitmap for the :class:`ShapedBitmapButton`.

        :returns: the hover bitmap
        :rtype: `wx.Bitmap`
        """

        return self._hoverBmp

    def SetBitmapHover(self, bitmap):
        """
        Sets the hover bitmap for the :class:`ShapedBitmapButton`.

        :param `bitmap`: the hover bitmap to set, an instance of :class:`Bitmap`.
        """

        self._hoverBmp = bitmap
        self.Refresh()

    def GetBitmapDisabled(self):
        """
        Gets the disabled bitmap for the :class:`ShapedBitmapButton`.

        :returns: the disabled bitmap
        :rtype: `wx.Bitmap`
        """

        return self._disabledBmp

    def SetBitmapDisabled(self, bitmap):
        """
        Sets the disabled bitmap for the :class:`ShapedBitmapButton`.

        :param `bitmap`: the disabled bitmap to set, an instance of :class:`Bitmap`.
        """

        self._disabledBmp = bitmap
        self.Refresh()

    def GetSBBChildren(self):
        childrenShapedBitmapButtons = [
                sbb for sbb in self.GetChildren()
                     if isinstance(sbb, ShapedBitmapButton)]
        return childrenShapedBitmapButtons

    def GetSBBSiblings(self):
        """
        Get a list of all the parents shaped bitmap buttons
        instances minus myself.
        """
        parent = self.GetParent()
        if not parent:  # Probably been/being deleted.
            return
        siblingShapedBitmapButtons = [
                sbb for sbb in parent.GetChildren()
                     if isinstance(sbb, ShapedBitmapButton)]
        siblingShapedBitmapButtons.remove(self)
        return siblingShapedBitmapButtons

    def OnPaint(self, event):
        """
        Handles the ``wx.EVT_PAINT`` event for :class:`ShapedBitmapButton`.

        :param `event`: a :class:`PaintEvent` event to be processed.
        """
        # print('OnPaint - ShapedBitmapButton %s' % time.time()) # Debug/Optimize how many times Refresh is firing off.
        # print('children', self.GetChildren())
        dc = wx.BufferedPaintDC(self)

        bitmap = self._bitmap

        parent = self.GetParent()
        if not parent:  # Probably been/being deleted.
            return
        dc.SetBackground(wx.Brush(parent.GetBackgroundColour()))
        dc.Clear()
        dc_DrawBitmap = dc.DrawBitmap

        imAChild = hasattr(parent, '_sbbChildBmp')
        if imAChild:  # I am a child here.
            parent.MakeChildBmp()
            dc.SetBackground(wx.Brush(parent.GetParent().GetBackgroundColour()))
            pos = self.GetPosition()
            sz = self.GetSize()
            parent_sbbChildBmp = parent._sbbChildBmp
            if parent_sbbChildBmp:
                dc_DrawBitmap(parent_sbbChildBmp.
                              GetSubBitmap(wx.Rect(pos[0], pos[1], sz[0], sz[1])), 0, 0, True)
        # @ NOTE: This section of code could cause errors with various sizers
        #         when sizing the frame to zilch/nothing.
        # @ except wx._core.wxAssertionError, wx._core.PyAssertionError:
        elif self._parentBgBmp:
            sz = self.Size  # sz = self.GetSize()
            # print('sz = %s, parentSz = %s' % (sz, self.parent.GetSize()))
            if sz[0] and sz[1]:  # if x or y is 0 it WILL cause major fubar havok; BoxSizer, WrapSizer
                pos = self.Position  # pos = self.GetPosition()
                # print('pos = %s, parentPos = %s' % (pos, self.parent.GetPosition()))
                if (pos[0] >= 0) and (pos[1] >= 0) and (pos[0]+sz[0] >= sz[0]) and (pos[1]+sz[1] >= sz[1]): # GridSizer fubar havok
                    dc_DrawBitmap(self._parentBgBmp.
                        GetSubBitmap(wx.Rect(pos[0], pos[1], sz[0], sz[1])), 0, 0, True)
                else:  # Something is better than nothing even if it is off a bit. TODO: Try to recalculate correct overlaying of GetSubBitmap
                    dc_DrawBitmap(self._parentBgBmp, 0, 0, True)

        if self._mouseAction == CLICK:
            bitmap = self._pressedBmp or bitmap
        elif self._mouseAction == HOVER:
            bitmap = self._hoverBmp or bitmap
        elif not self.IsEnabled():
            bitmap = self._disabledBmp or bitmap

        dc_DrawBitmap(bitmap, 0, 0)

        if self._labelEnable and self._labelsList or self._label:
            dc.SetBrush(wx.TRANSPARENT_BRUSH)
            transparentColour = wx.TransparentColour
            transparent = wx.TRANSPARENT
            solid = wx.SOLID
            if self._labelsList:
                dc_SetBackgroundMode = dc.SetBackgroundMode
                dc_SetTextForeground = dc.SetTextForeground
                dc_SetTextBackground = dc.SetTextBackground
                dc_SetFont = dc.SetFont
                dc_DrawRotatedText = dc.DrawRotatedText
                for label, coords, foreground, background, font, rotation in self._labelsList:
                    if background == transparentColour:
                        dc_SetBackgroundMode(transparent)
                    else:
                        dc_SetBackgroundMode(solid)
                    dc_SetTextForeground(foreground)
                    dc_SetTextBackground(background)
                    dc_SetFont(font)
                    dc_DrawRotatedText(label,
                                       coords[0],
                                       coords[1],
                                       rotation)
            else:  # self._label
                if self._labelBackColour == transparentColour:
                    dc.SetBackgroundMode(transparent)
                else:
                    dc.SetBackgroundMode(solid)
                dc.SetTextBackground(self._labelBackColour)
                dc.SetTextForeground(self._labelForeColour)
                dc.SetFont(self._labelFont)
                dc.DrawRotatedText(self._label,
                                   self._labelPosition[0],
                                   self._labelPosition[1],
                                   self._labelRotation)

        if self._makeChildBmp:  # I am a parent here.
            self._sbbChildBmp = dc.GetAsBitmap()
            self._makeChildBmp = False

    def MakeChildBmp(self):
        self._makeChildBmp = True
        # self.Refresh()

    def OnKeyDown(self, event):
        """
        Handles the ``wx.EVT_KEY_DOWN`` event for :class:`ShapedBitmapButton`.

        :param `event`: a :class:`KeyEvent` event to be processed.
        """

        hasFocus = self.HasFocus()
        if hasFocus and event.GetKeyCode() == ord(" "):
            if self.HasCapture():
                self.ReleaseMouse()
            self._mouseAction = CLICK
            self.CaptureMouse()
            self.Refresh()

        elif hasFocus and self.HasFlag(wx.WANTS_CHARS) and wx.GetKeyState(wx.WXK_RETURN):
            if self.HasCapture():
                self.ReleaseMouse()
            self._mouseAction = CLICK
            self.CaptureMouse()
            self.Refresh()

        # print('PROCESS_ENTER', self.HasFlag(wx.PROCESS_ENTER))
        # print('WANTS_CHARS', self.HasFlag(wx.WANTS_CHARS))

        event.Skip()
        # print('OnKeyDown')

    def OnKeyUp(self, event):
        """
        Handles the ``wx.EVT_KEY_UP`` event for :class:`ShapedBitmapButton`.

        :param `event`: a :class:`KeyEvent` event to be processed.
        """

        hasFocus = self.HasFocus()
        if hasFocus and event.GetKeyCode() == ord(" "):
            if self.HasCapture():
                self.ReleaseMouse()
            self._mouseAction = HOVER
            self.Notify()

        elif hasFocus and self.HasCapture() and not wx.GetKeyState(wx.WXK_RETURN):
            if self.HasCapture():
                self.ReleaseMouse()
            self._mouseAction = None
            self.Notify()

        x, y = event.GetPosition()
        if not self._region.Contains(x, y):
            self._mouseAction = None
        else:
            self._mouseAction = HOVER

        self.Refresh()
        event.Skip()
        # print('OnKeyUp')

    def GetRegion(self):
        """
        Get the region.

        :returns: The region for the shaped bitmap button.
        :rtype: `wx.Region`
        """
        return self._region

    def SetRegion(self, region):
        """
        Set the region.

        :param `region`: The region to set for the shaped bitmap button.
        :type `region`: `wx.Region`
        """
        self._region = region

    def RegionContainsPoint(self, point):
        """
        Does the region contain a point.

        :param `point`: The point to check for in the region.
        :type `point`: `wx.Point`
        """
        return self._region.ContainsPoint(point)

    def RegionContains(self, x, y):
        """
        Does the region contain x, y.

        :param `x`: A  `wx.Point` x value.
        :type `x`: int
        :param `y`: A `wx.Point` y value.
        :type `y`: int
        """
        return self._region.Contains(x, y)

    def OnLeftDown(self, event):
        """
        Handles the ``wx.EVT_LEFT_DOWN`` event for :class:`ShapedBitmapButton`.

        :param `event`: a :class:`MouseEvent` event to be processed.
        """

        ## x, y = event.GetPosition()
        ## self._mouseIsInRegion = self_mouseIsInRegion = self.IsMousePositionInRegion()
        x, y = self.ScreenToClient(wxGetMousePosition())
        self._mouseIsInRegion = self_mouseIsInRegion = self._region.Contains(x, y)

        parent = self.GetParent()
        ## imAChild = hasattr(parent, '_sbbChildBmp')
        ## if not self_mouseIsInRegion and imAChild:
        ##     selfPosX, selfPosY = self.GetPosition()
        ##     underX, underY = selfPosX + x, selfPosY + y
        ##     if parent._region.Contains(underX, underY):
        ##         # Send the event back to the parent because we are hovering over it and have clicked.
        ##         parent._mouseAction = CLICK
        ##         # parent._mouseIsInRegion = True
        ##         parent.Refresh()
        ##         event.Skip()
        ##         return

        if not self_mouseIsInRegion:  # Pass the wx.EVT_LEFT_DOWN to the parent
            selfPosX, selfPosY = self.GetPosition()
            underX, underY = selfPosX + x, selfPosY + y
            self.SendMouseEvent(parent, wx.wxEVT_LEFT_DOWN, underX, underY)

        if not self.IsEnabled():
            return

        if self_mouseIsInRegion:
            self._mouseAction = CLICK
            if self.HasCapture():
                self.ReleaseMouse()
            self.CaptureMouse()

            if hasattr(self, '_sbbChildBmp'):
                self.MakeChildBmp()
            self.Refresh()

        event.Skip()

    def OnLeftDClick(self, event):
        """
        Handles the ``wx.EVT_LEFT_DCLICK`` event for :class:`ShapedBitmapButton`.

        :param `event`: a :class:`MouseEvent` event to be processed.
        """

        self.OnLeftDown(event)
        event.Skip()

    def OnLeftUp(self, event):
        """
        Handles the ``wx.EVT_LEFT_UP`` event for :class:`ShapedBitmapButton`.

        :param `event`: a :class:`MouseEvent` event to be processed.
        """

        ## x, y = event.GetPosition()
        ## self._mouseIsInRegion = self_mouseIsInRegion = self.IsMousePositionInRegion()
        x, y = self.ScreenToClient(wxGetMousePosition())
        self._mouseIsInRegion = self_mouseIsInRegion = self._region.Contains(x, y)
        # print('OnLeftUp', self.GetName())

        parent = self.GetParent()
        imAChild = hasattr(parent, '_sbbChildBmp')
        if not self_mouseIsInRegion and imAChild:  # I am a child here.
            selfPosX, selfPosY = self.GetPosition()
            underX, underY = selfPosX + x, selfPosY + y
            if parent._region.Contains(underX, underY):
                # Send the event back to the parent because we are hovering over it and have clicked.
                # self.parent._mouseIsInRegion = True
                parent._mouseAction = HOVER
                parent.Notify()
                return

        if not self_mouseIsInRegion:  # Pass the wx.EVT_LEFT_UP to the parent
            selfPosX, selfPosY = self.GetPosition()
            underX, underY = selfPosX + x, selfPosY + y
            self.SendMouseEvent(parent, wx.wxEVT_LEFT_UP, underX, underY)

        if not self.IsEnabled() or not self.HasCapture():
            return

        if self.HasCapture():
            self.ReleaseMouse()

        if self_mouseIsInRegion:
            self._mouseAction = HOVER
            if self.IsMousePositionInAnyChildsRegion():
                pass
            else:
                self.Notify()
        else:
            self._mouseAction = None

        self.Refresh()
        event.Skip()

    def OnRightDown(self, event):
        """
        Handles the ``wx.EVT_RIGHT_DOWN`` event for :class:`ShapedBitmapButton`.

        :param `event`: a :class:`MouseEvent` event to be processed.
        """

        ## x, y = event.GetPosition()
        x, y = self.ScreenToClient(wxGetMousePosition())
        self._mouseIsInRegion = self_mouseIsInRegion = self._region.Contains(x, y)

        if not self_mouseIsInRegion:  # Pass the wx.EVT_RIGHT_DOWN to the parent
            selfPosX, selfPosY = self.GetPosition()
            underX, underY = selfPosX + x, selfPosY + y
            self.SendMouseEvent(self.parent, wx.wxEVT_RIGHT_DOWN, underX, underY)

    def OnRightDClick(self, event):
        """
        Handles the ``wx.EVT_RIGHT_DCLICK`` event for :class:`ShapedBitmapButton`.

        :param `event`: a :class:`MouseEvent` event to be processed.
        """

        ## x, y = event.GetPosition()
        x, y = self.ScreenToClient(wxGetMousePosition())
        self._mouseIsInRegion = self_mouseIsInRegion = self._region.Contains(x, y)

        if not self_mouseIsInRegion:  # Pass the wx.EVT_RIGHT_DCLICK to the parent
            selfPosX, selfPosY = self.GetPosition()
            underX, underY = selfPosX + x, selfPosY + y
            self.SendMouseEvent(self.parent, wx.wxEVT_RIGHT_DCLICK, underX, underY)

    def OnRightUp(self, event):
        """
        Handles the ``wx.EVT_RIGHT_UP`` event for :class:`ShapedBitmapButton`.

        :param `event`: a :class:`MouseEvent` event to be processed.
        """

        ## x, y = event.GetPosition()
        x, y = self.ScreenToClient(wxGetMousePosition())
        self._mouseIsInRegion = self_mouseIsInRegion = self._region.Contains(x, y)

        if not self_mouseIsInRegion:  # Pass the wx.EVT_RIGHT_UP to the parent
            selfPosX, selfPosY = self.GetPosition()
            underX, underY = selfPosX + x, selfPosY + y
            self.SendMouseEvent(self.parent, wx.wxEVT_RIGHT_UP, underX, underY)

    def OnMiddleDown(self, event):
        """
        Handles the ``wx.EVT_MIDDLE_DOWN`` event for :class:`ShapedBitmapButton`.

        :param `event`: a :class:`MouseEvent` event to be processed.
        """

        ## x, y = event.GetPosition()
        x, y = self.ScreenToClient(wxGetMousePosition())
        self._mouseIsInRegion = self_mouseIsInRegion = self._region.Contains(x, y)

        if not self_mouseIsInRegion:  # Pass the wx.EVT_MIDDLE_DOWN to the parent
            selfPosX, selfPosY = self.GetPosition()
            underX, underY = selfPosX + x, selfPosY + y
            self.SendMouseEvent(self.parent, wx.wxEVT_MIDDLE_DOWN, underX, underY)

    def OnMiddleDClick(self, event):
        """
        Handles the ``wx.EVT_MIDDLE_DCLICK`` event for :class:`ShapedBitmapButton`.

        :param `event`: a :class:`MouseEvent` event to be processed.
        """

        ## x, y = event.GetPosition()
        x, y = self.ScreenToClient(wxGetMousePosition())
        self._mouseIsInRegion = self_mouseIsInRegion = self._region.Contains(x, y)

        if not self_mouseIsInRegion:  # Pass the wx.EVT_MIDDLE_DCLICK to the parent
            selfPosX, selfPosY = self.GetPosition()
            underX, underY = selfPosX + x, selfPosY + y
            self.SendMouseEvent(self.parent, wx.wxEVT_MIDDLE_DCLICK, underX, underY)

    def OnMiddleUp(self, event):
        """
        Handles the ``wx.EVT_MIDDLE_UP`` event for :class:`ShapedBitmapButton`.

        :param `event`: a :class:`MouseEvent` event to be processed.
        """

        ## x, y = event.GetPosition()
        x, y = self.ScreenToClient(wxGetMousePosition())
        self._mouseIsInRegion = self_mouseIsInRegion = self._region.Contains(x, y)

        if not self_mouseIsInRegion:  # Pass the wx.EVT_MIDDLE_UP to the parent
            selfPosX, selfPosY = self.GetPosition()
            underX, underY = selfPosX + x, selfPosY + y
            self.SendMouseEvent(self.parent, wx.wxEVT_MIDDLE_UP, underX, underY)

    def OnAux1Down(self, event):
        """
        Handles the ``wx.EVT_MOUSE_AUX1_DOWN`` event for :class:`ShapedBitmapButton`.

        :param `event`: a :class:`MouseEvent` event to be processed.
        """

        ## x, y = event.GetPosition()
        x, y = self.ScreenToClient(wxGetMousePosition())
        self._mouseIsInRegion = self_mouseIsInRegion = self._region.Contains(x, y)

        if not self_mouseIsInRegion:  # Pass the wx.EVT_MOUSE_AUX1_DOWN to the parent
            selfPosX, selfPosY = self.GetPosition()
            underX, underY = selfPosX + x, selfPosY + y
            self.SendMouseEvent(self.parent, wx.wxEVT_MOUSE_AUX1_DOWN, underX, underY)

    def OnAux1Up(self, event):
        """
        Handles the ``wx.EVT_MOUSE_AUX1_UP`` event for :class:`ShapedBitmapButton`.

        :param `event`: a :class:`MouseEvent` event to be processed.
        """

        ## x, y = event.GetPosition()
        x, y = self.ScreenToClient(wxGetMousePosition())
        self._mouseIsInRegion = self_mouseIsInRegion = self._region.Contains(x, y)

        if not self_mouseIsInRegion:  # Pass the wx.EVT_MOUSE_AUX1_UP to the parent
            selfPosX, selfPosY = self.GetPosition()
            underX, underY = selfPosX + x, selfPosY + y
            self.SendMouseEvent(self.parent, wx.wxEVT_MOUSE_AUX1_UP, underX, underY)

    def OnAux1DClick(self, event):
        """
        Handles the ``wx.EVT_MOUSE_AUX1_DCLICK`` event for :class:`ShapedBitmapButton`.

        :param `event`: a :class:`MouseEvent` event to be processed.
        """

        ## x, y = event.GetPosition()
        x, y = self.ScreenToClient(wxGetMousePosition())
        self._mouseIsInRegion = self_mouseIsInRegion = self._region.Contains(x, y)

        if not self_mouseIsInRegion:  # Pass the wx.EVT_MOUSE_AUX1_DCLICK to the parent
            selfPosX, selfPosY = self.GetPosition()
            underX, underY = selfPosX + x, selfPosY + y
            self.SendMouseEvent(self.parent, wx.wxEVT_MOUSE_AUX1_DCLICK, underX, underY)

    def OnAux2Down(self, event):
        """
        Handles the ``wx.EVT_MOUSE_AUX2_DOWN`` event for :class:`ShapedBitmapButton`.

        :param `event`: a :class:`MouseEvent` event to be processed.
        """

        ## x, y = event.GetPosition()
        x, y = self.ScreenToClient(wxGetMousePosition())
        self._mouseIsInRegion = self_mouseIsInRegion = self._region.Contains(x, y)

        if not self_mouseIsInRegion:  # Pass the wx.EVT_MOUSE_AUX2_DOWN to the parent
            selfPosX, selfPosY = self.GetPosition()
            underX, underY = selfPosX + x, selfPosY + y
            self.SendMouseEvent(self.parent, wx.wxEVT_MOUSE_AUX2_DOWN, underX, underY)

    def OnAux2Up(self, event):
        """
        Handles the ``wx.EVT_MOUSE_AUX2_UP`` event for :class:`ShapedBitmapButton`.

        :param `event`: a :class:`MouseEvent` event to be processed.
        """

        ## x, y = event.GetPosition()
        x, y = self.ScreenToClient(wxGetMousePosition())
        self._mouseIsInRegion = self_mouseIsInRegion = self._region.Contains(x, y)

        if not self_mouseIsInRegion:  # Pass the wx.EVT_MOUSE_AUX2_UP to the parent
            selfPosX, selfPosY = self.GetPosition()
            underX, underY = selfPosX + x, selfPosY + y
            self.SendMouseEvent(self.parent, wx.wxEVT_MOUSE_AUX2_UP, underX, underY)

    def OnAux2DClick(self, event):
        """
        Handles the ``wx.EVT_MOUSE_AUX2_DCLICK`` event for :class:`ShapedBitmapButton`.

        :param `event`: a :class:`MouseEvent` event to be processed.
        """

        ## x, y = event.GetPosition()
        x, y = self.ScreenToClient(wxGetMousePosition())
        self._mouseIsInRegion = self_mouseIsInRegion = self._region.Contains(x, y)

        if not self_mouseIsInRegion:  # Pass the wx.EVT_MOUSE_AUX2_DCLICK to the parent
            selfPosX, selfPosY = self.GetPosition()
            underX, underY = selfPosX + x, selfPosY + y
            self.SendMouseEvent(self.parent, wx.wxEVT_MOUSE_AUX2_DCLICK, underX, underY)

    def OnMotion(self, event):
        """
        Handles the ``wx.EVT_MOTION`` event for :class:`ShapedBitmapButton`.

        :param `event`: a :class:`MouseEvent` event to be processed.
        """

        x, y = event.GetPosition()
        ## x, y = event.GetPosition()
        ## x, y = self.ScreenToClient(wxGetMousePosition())
        ## self._mouseIsInRegion = self_mouseIsInRegion = self._region.Contains(x, y)

        regionContainsPoint = self._region.Contains(x, y)
        parent = self.GetParent()
        imAChild = hasattr(parent, '_sbbChildBmp')

        if not regionContainsPoint and imAChild:  # I am a child here.
            selfPosX, selfPosY = self.GetPosition()
            # print('selfPos = %s, %s' % (selfPosX, selfPosY))
            # print('OnMotion x, y = %s,%s' % (x, y))
            if parent._region.Contains(selfPosX + x, selfPosY + y):
                # Simulate the event back to the parent because we are hovering over it.

                # print('OnMotion x, y = %s,%s' % (x, y))
                # print('self.parent._mouseAction', parent._mouseAction)
                # print('self.parent._mouseIsInRegion', parent._mouseIsInRegion)
                if ((not parent._mouseAction == HOVER) or (not parent._mouseIsInRegion)):  # Don't constantly paint
                    parent._mouseAction = HOVER
                    parent._mouseIsInRegion = True
                    parent.MakeChildBmp()
                    parent.Refresh()

                # print('self.parent._makeChildBmp', parent._makeChildBmp)
                # if self.parent._makeChildBmp:
                #     parent.MakeChildBmp()
                #     parent.Refresh()
                #     parent._makeChildBmp = False

                if self.HasCapture():
                    self._mouseAction = CLICK
                else:
                    self._mouseAction = None
                    if self.GetToolTip():  # HOVER event happens before CLICK.
                        self.GetToolTip().Enable(False)

                self._mouseIsInRegion = False
                # self.Refresh()
                event.Skip()
                return

        if not regionContainsPoint:
            if self._mouseIsInRegion:  # Update Visual.
                self._mouseIsInRegion = False
                if hasattr(self, '_sbbChildBmp'):
                    self.MakeChildBmp()
                self.Refresh()
            self._mouseAction = None
            if self.GetToolTip():  # Only show the tooltip when in region, not when in rect.
                self.GetToolTip().Enable(False)

            # Pass the wx.EVT_MOTION to the parent
            selfPosX, selfPosY = self.GetPosition()
            underX, underY = selfPosX + x, selfPosY + y
            self.SendMouseEvent(parent, wx.wxEVT_MOTION, underX, underY)

        else:
            if self.HasCapture():
                self._mouseAction = CLICK
            else:
                self._mouseAction = HOVER
                if self.GetToolTip():  # HOVER event happens before CLICK.
                    self.GetToolTip().Enable(True)
            if imAChild:
                parent._mouseAction = None
                parent.MakeChildBmp()
                parent.Refresh()
            if not self._mouseIsInRegion:
                self._mouseIsInRegion = True

                if hasattr(self, '_sbbChildBmp'):
                    self.MakeChildBmp()

                self.Refresh()

        event.Skip()
        ## print('OnMotion (%s, %s)' % (x, y))

    def OnEnterWindow(self, event):
        """
        Handles the ``wx.EVT_ENTER_WINDOW`` event for :class:`ShapedBitmapButton`.

        :param `event`: a :class:`MouseEvent` event to be processed.
        """

        if not self.IsEnabled():
            return

        ## x, y = event.GetPosition()
        x, y = self.ScreenToClient(wxGetMousePosition())
        self._mouseIsInRegion = self_mouseIsInRegion = self._region.Contains(x, y)

        if self_mouseIsInRegion:
            self._mouseAction = HOVER

            self.Refresh()

        event.Skip()

    def OnLeaveWindow(self, event):
        """
        Handles the ``wx.EVT_LEAVE_WINDOW`` event for :class:`ShapedBitmapButton`.

        :param `event`: a :class:`MouseEvent` event to be processed.
        """

        if self._mouseAction: # not == None
            self._mouseAction = None
            self._mouseIsInRegion = False
            if hasattr(self, '_sbbChildBmp'):
                self.MakeChildBmp()
            self.Refresh()
            # self.Update()

        event.Skip()

    def OnMouseWheel(self, event):
        """
        Handles the ``wx.EVT_MOUSEWHEEL`` event for :class:`ShapedBitmapButton`.

        :param `event`: a :class:`MouseEvent` event to be processed.
        """

        ## x, y = event.GetPosition()
        x, y = self.ScreenToClient(wxGetMousePosition())
        self._mouseIsInRegion = self_mouseIsInRegion = self._region.Contains(x, y)

        if not self_mouseIsInRegion:  # Pass the wx.EVT_MOUSEWHEEL to the parent
            selfPosX, selfPosY = self.GetPosition()
            underX, underY = selfPosX + x, selfPosY + y
            self.SendMouseEvent(self.parent, wx.wxEVT_MOUSEWHEEL, underX, underY)

    def OnMouseEvents(self, event):
        """
        Handles the ``wx.EVT_MOUSE_EVENTS`` event for :class:`ShapedBitmapButton`.

        :param `event`: a :class:`MouseEvent` event to be processed.
        """
        event.Skip()
        NotImplemented
        x, y = event.GetPosition()

        ## if not self._region.Contains(x, y):  # Pass the wx.EVT_MOUSE_EVENTS to the parent
        ##     selfPosX, selfPosY = self.GetPosition()
        ##     underX, underY = selfPosX + x, selfPosY + y
        ##     self.SendMouseEvent(self.parent, wx.wxEVT_???, underX, underY)

    def OnGainFocus(self, event):
        """
        Handles the ``wx.EVT_SET_FOCUS`` event for :class:`ShapedBitmapButton`.

        :param `event`: a :class:`FocusEvent` event to be processed.
        """
        # self._hasFocus = True
        # self.Refresh()
        # self.Update()
        # event.Skip()
        # print('OnGainFocus')
        pass

    def OnLoseFocus(self, event):
        """
        Handles the ``wx.EVT_KILL_FOCUS`` event for :class:`ShapedBitmapButton`.

        :param `event`: a :class:`FocusEvent` event to be processed.
        """
        # self._hasFocus = False
        # self.Refresh()
        # self.Update()
        # event.Skip()
        # print('OnLoseFocus')
        pass

    def OnContextMenu(self, event):
        """
        Handles the ``wx.EVT_CONTEXT_MENU`` event for :class:`ShapedBitmapButton`.

        :param `event`: a :class:`ContextMenuEvent` event to be processed.
        """

        x, y = event.GetPosition()

        if not self._region.Contains(x, y):  # Pass the wx.EVT_CONTEXT_MENU to the parent
            selfPosX, selfPosY = self.GetPosition()
            underX, underY = selfPosX + x, selfPosY + y
            self.SendContextMenuEvent(self.parent, underX, underY)

    def SendContextMenuEvent(self, window, x, y):
        cmd = wx.ContextMenuEvent(wx.wxEVT_CONTEXT_MENU)
        cmd.SetEventObject(window)
        cmd.SetId(window.GetId())
        cmd.SetX(x)
        cmd.SetY(y)
        window.GetEventHandler().ProcessEvent(cmd)

    def SendMouseEvent(self, window, mouseType, x, y):
        cmd = wx.MouseEvent(mouseType)
        cmd.SetEventObject(window)
        cmd.SetId(window.GetId())
        cmd.SetX(x)
        cmd.SetY(y)
        window.GetEventHandler().ProcessEvent(cmd)

    def SendEvent(self, window, PyEventBinder):
        # Example of PyEventBinder: wx.EVT_BUTTON
        # window is the window (control) that triggers the event
        cmd = wx.CommandEvent(PyEventBinder.evtType[0])
        cmd.SetEventObject(window)
        cmd.SetId(window.GetId())
        window.GetEventHandler().ProcessEvent(cmd)

    def Notify(self):
        """ Actually sends a ``wx.EVT_BUTTON`` event to the listener (if any). """
        if self._raiseOnSetFocus:
            self.Refresh()
            if self._mouseIsInRegion:
                self.Raise()
        evt = ShapedBitmapButtonEvent(wx.wxEVT_COMMAND_BUTTON_CLICKED, self.GetId())
        evt.SetButtonObj(self)
        evt.SetEventObject(self)
        self.GetEventHandler().ProcessEvent(evt)

    def IsMousePositionInRegion(self):
        x, y = self.ScreenToClient(wxGetMousePosition())
        return self._region.Contains(x, y)

    def IsMousePositionInAnyChildsRegion(self):
        childrenShapedBitmapButtons = [
                sbb for sbb in self.GetChildren()
                     if isinstance(sbb, ShapedBitmapButton)]
        for child in childrenShapedBitmapButtons:
            x, y = child.ScreenToClient(wxGetMousePosition())
            if child._region.Contains(x, y):
                return True
        return False


class ShapedBitmapButtonAdv(ShapedBitmapButton):
    """
    This is the advanced class implementation of :class:`ShapedBitmapButton`.

    Handles sibling ShapedBitmapButton's alpha drawing when within anothers rect

    """

    def OnPaint(self, event):
        """
        Handles the ``wx.EVT_PAINT`` event for :class:`ShapedBitmapButton`.

        :param `event`: a :class:`PaintEvent` event to be processed.
        """
        ## print('OnPaint - ShapedBitmapButton %s' % time.time())  # DEBUG/Optimize how many times Refresh is firing off.
        dc = wx.BufferedPaintDC(self)

        bitmap = self._bitmap

        parent = self.GetParent()
        if not parent:  # Probably been/being deleted.
            return
        dc.SetBackground(wx.Brush(parent.GetBackgroundColour()))
        dc.Clear()
        dc_DrawBitmap = dc.DrawBitmap

        imAChild = hasattr(parent, '_sbbChildBmp')
        if imAChild:  # I am a child here.
            parent.MakeChildBmp()
            dc.SetBackground(wx.Brush(parent.GetParent().GetBackgroundColour()))
            posX, posY = self.GetPosition()
            szW, szH = self.GetSize()
            parent_sbbChildBmp = parent._sbbChildBmp
            if parent_sbbChildBmp:
                dc_DrawBitmap(parent_sbbChildBmp.
                              GetSubBitmap(wx.Rect(posX, posY, szW, szH)), 0, 0, True)
        # @ NOTE: This section of code could cause errors with various sizers
        #         when sizing the frame to zilch/nothing.
        # @ except wx._core.wxAssertionError, wx._core.PyAssertionError:
        elif self._parentBgBmp:
            szW, szH = self.Size  # sz = self.GetSize()
            # print('sz = %s, parentSz = %s' % (sz, self.parent.GetSize()))
            if szW and szH:  # if x or y is 0 it WILL cause major fubar havok; BoxSizer, WrapSizer
                posX, posY = self.Position  # pos = self.GetPosition()
                if (posX >= 0) and (posY >= 0) and (posX + szW >= szW) and (posY + szH >= szH): # GridSizer fubar havok
                    dc_DrawBitmap(self._parentBgBmp.
                        GetSubBitmap(wx.Rect(posX, posY, szW, szH)), 0, 0, True)
                else:  # Something is better than nothing even if it is off a bit. TODO: Try to recalculate correct overlaying of GetSubBitmap
                    # print('posX, posY', posX, posY)
                    dc_DrawBitmap(self._parentBgBmp, 0, 0, True)
            ## else:  # Something is better than nothing even if it is off a bit. TODO: Try to recalculate correct overlaying of GetSubBitmap
            ##     dc_DrawBitmap(self._parentBgBmp, 0, 0, True)

        if self._mouseAction == CLICK:
            bitmap = self._pressedBmp or bitmap
        elif self._mouseAction == HOVER:
            bitmap = self._hoverBmp or bitmap
        elif not self.IsEnabled():
            bitmap = self._disabledBmp or bitmap

        # EXPERIMENTAL TODO: make an option for this sibling drawing as it may not be necessary if sbb's are in a sizer ect...
        if not parent.GetSizer():  # It's obvious this wouldnt be needed if they are in a sizer.
            siblings = self.GetSBBSiblings()
            if siblings:
                ### mx, my = self.GetPosition()
                ### mw, mh = bitmap.GetWidth(), bitmap.GetHeight()
                ### myrect = wx.Rect(mx, my, mw, mh)
                mx, my, mw, mh = myrect = self.GetRect()
                myrect_Contains = myrect.Contains
                # print('--')
                wxRect = wx.Rect
                selfIsMousePositionInRegion = self.IsMousePositionInRegion()
                for sibling in siblings:
                    sibbmp = sibling._bitmap
                    sx, sy = sibpos = sibling.GetPosition()
                    sibw = sibbmp.GetWidth()
                    sibh = sibbmp.GetHeight()
                    ### sx, sy, sw, sh = sibling.GetRect()
                    ### sibw = sx + sw
                    ### sibh = sy + sh
                    ## sibpos = (sx, sy)
                    ## print('sibpos %s' % sibling.Name, sibpos)
                    topLeftPt = (sx, sy)
                    topRightPt = (sx + sibw, sy)
                    bottomLeftPt = (sx, sy + sibh)
                    bottomRightPt = (sx + sibw, sy + sibh)
                    topLeft = myrect_Contains(topLeftPt)
                    topRight = myrect_Contains(topRightPt)
                    bottomLeft = myrect_Contains(bottomLeftPt)
                    bottomRight = myrect_Contains(bottomRightPt)
                    ### topLeft = mx <= sx <= mx + mw and my <= sy <= my + mh
                    ### topRight = mx <= sx + sibw <= mx + mw and my <= sy <= my + mh
                    ### bottomLeft = mx <= sx <= mx + mw and my <= sy + sibh <= my + mh
                    ### bottomRight = mx <= sx + sibw <= mx + mw and my <= sy + sibh <= my + mh
                    # print('topLeft', topLeft)
                    # print('topRight', topRight)
                    # print('bottomLeft', bottomLeft)
                    # print('bottomRight', bottomRight)
                    sibIsMousePositionInRegion = sibling.IsMousePositionInRegion()
                    if topLeft and not bottomRight and not topRight and not bottomLeft:  # TopLeftCorner point
                        x = 0
                        y = 0
                        w = mw - (sx - mx)
                        h = mh - (sy - my)
                        # print('x,y,w,h topLeft: ',x,y,w,h)
                        if not w or not h:
                             continue

                        if sibIsMousePositionInRegion and not selfIsMousePositionInRegion:
                            sibsubbmp = sibling._hoverBmp.GetSubBitmap(wxRect(x,y,w,h))
                        else:
                            sibsubbmp = sibling._bitmap.GetSubBitmap(wxRect(x,y,w,h))

                        # sibsubbmp = sibling._bitmap.GetSubBitmap(wxRect(x,y,w,h))
                        dc_DrawBitmap(sibsubbmp, sx - mx, sy - my)
                    elif topRight and not bottomRight and not topLeft and not bottomLeft:  # TopRightCorner point
                        w = sx + sibw - mx
                        h = mh - (sy - my)
                        x = sibw - w
                        y = 0
                        # print('x,y,w,h topLeft: ',x,y,w,h)
                        if not w or not h:
                            continue

                        if sibIsMousePositionInRegion and not selfIsMousePositionInRegion:
                            sibsubbmp = sibling._hoverBmp.GetSubBitmap(wxRect(x,y,w,h))
                        else:
                            sibsubbmp = sibling._bitmap.GetSubBitmap(wxRect(x,y,w,h))

                        # sibsubbmp = sibling._bitmap.GetSubBitmap(wxRect(x,y,w,h))
                        dc_DrawBitmap(sibsubbmp, 0, sy - my)
                    elif bottomLeft and not topLeft and not bottomRight and not topRight:  # BottomLeftCorner point
                        w = mw - (sx - mx)
                        h = sy + sibh - my
                        x = 0
                        y = sibh - h
                        # print('x,y,w,h bottomLeft: ',x,y,w,h)
                        if not w or not h:
                            continue

                        if sibIsMousePositionInRegion and not selfIsMousePositionInRegion:
                            sibsubbmp = sibling._hoverBmp.GetSubBitmap(wxRect(x,y,w,h))
                        else:
                            sibsubbmp = sibling._bitmap.GetSubBitmap(wxRect(x,y,w,h))

                        # sibsubbmp = sibling._bitmap.GetSubBitmap(wxRect(x,y,w,h))
                        dc_DrawBitmap(sibsubbmp, sx - mx, 0)
                    elif bottomRight and not topLeft and not bottomLeft and not topRight:  # BottomRightCorner point
                        w = sx + sibw - mx
                        h = sy + sibh - my
                        x = sibw - w
                        y = sibh - h
                        # print('x,y,w,h bottomRight: ',x,y,w,h)
                        if not w or not h:
                            continue

                        if sibIsMousePositionInRegion and not selfIsMousePositionInRegion:
                            sibsubbmp = sibling._hoverBmp.GetSubBitmap(wxRect(x,y,w,h))
                        else:
                            sibsubbmp = sibling._bitmap.GetSubBitmap(wxRect(x,y,w,h))

                        # sibsubbmp = sibling._bitmap.GetSubBitmap(wxRect(x,y,w,h))
                        dc_DrawBitmap(sibsubbmp, 0, 0)


        dc_DrawBitmap(bitmap, 0, 0)

        if self._labelEnable and self._labelsList or self._label:
            dc.SetBrush(wx.TRANSPARENT_BRUSH)
            transparentColour = wx.TransparentColour
            transparent = wx.TRANSPARENT
            solid = wx.SOLID
            if self._labelsList:
                dc_SetBackgroundMode = dc.SetBackgroundMode
                dc_SetTextForeground = dc.SetTextForeground
                dc_SetTextBackground = dc.SetTextBackground
                dc_SetFont = dc.SetFont
                dc_DrawRotatedText = dc.DrawRotatedText
                for label, coords, foreground, background, font, rotation in self._labelsList:
                    if background == transparentColour:
                        dc_SetBackgroundMode(transparent)
                    else:
                        dc_SetBackgroundMode(solid)
                    dc_SetTextForeground(foreground)
                    dc_SetTextBackground(background)
                    dc_SetFont(font)
                    dc_DrawRotatedText(label,
                                       coords[0],
                                       coords[1],
                                       rotation)
            else:  # self._label
                if self._labelBackColour == transparentColour:
                    dc.SetBackgroundMode(transparent)
                else:
                    dc.SetBackgroundMode(solid)
                dc.SetTextBackground(self._labelBackColour)
                dc.SetTextForeground(self._labelForeColour)
                dc.SetFont(self._labelFont)
                dc.DrawRotatedText(self._label,
                                   self._labelPosition[0],
                                   self._labelPosition[1],
                                   self._labelRotation)

        if self._makeChildBmp:  # I am a parent here.
            self._sbbChildBmp = dc.GetAsBitmap()
            self._makeChildBmp = False

    def OnMouseEvents(self, event):
        """
        Handles the ``wx.EVT_MOUSE_EVENTS`` event for :class:`ShapedBitmapButton`.

        :param `event`: a :class:`MouseEvent` event to be processed.
        """
        evtType = event.GetEventType()
        # print('OnMouseEvents: ', event.GetEventType())
        x, y = event.GetPosition()
        if evtType == wx.EVT_MOTION:  # Handle this here in this class.
            self.OnMotion(event)
        else:
            # if self._region.Contains(x, y):
            event.Skip()
        # event.Skip()
        # NotImplemented

        ## if not self._region.Contains(x, y):  # Pass the wx.EVT_MOUSE_EVENTS to the parent
        ##     selfPosX, selfPosY = self.GetPosition()
        ##     underX, underY = selfPosX + x, selfPosY + y
        ##     self.SendMouseEvent(self.parent, wx.wxEVT_???, underX, underY)

    def OnMotion(self, event):
        """
        Handles the ``wx.EVT_MOTION`` event for :class:`ShapedBitmapButton`.

        :param `event`: a :class:`MouseEvent` event to be processed.
        """
        # print('draworder: ', [sib.GetName() for sib in self.GetSBBSiblings()])
        x, y = event.GetPosition()
        mouseX, mouseY = self.ScreenToClient(wxGetMousePosition())
        # print('Motion x, y, mouseX, mouseY', x, y, mouseX, mouseY)

        regionContainsPoint = self._region.Contains(x, y)
        parent = self.GetParent()
        imAChild = hasattr(parent, '_sbbChildBmp')

        if not regionContainsPoint and imAChild:  # I am a child here.
            selfPosX, selfPosY = self.GetPosition()
            # print('selfPos = %s, %s' % (selfPosX, selfPosY))
            # print('OnMotion x, y = %s,%s' % (x, y))
            if parent._region.Contains(selfPosX + x, selfPosY + y):
                # Simulate the event back to the parent because we are hovering over it.

                # print('OnMotion x, y = %s,%s' % (x, y))
                # print('parent._mouseAction', parent._mouseAction)
                # print('parent._mouseIsInRegion', parent._mouseIsInRegion)
                if ((not parent._mouseAction == HOVER) or (not parent._mouseIsInRegion)):  # Don't constantly paint
                    parent._mouseAction = HOVER
                    parent._mouseIsInRegion = True
                    parent.Refresh()

                # print('parent._makeChildBmp', parent._makeChildBmp)
                # if parent._makeChildBmp:
                #     parent.MakeChildBmp()
                #     parent.Refresh()
                #     parent._makeChildBmp = False

                if self.HasCapture():
                    self._mouseAction = CLICK
                else:
                    self._mouseAction = None
                    if self.GetToolTip():  # HOVER event happens before CLICK.
                        self.GetToolTip().Enable(False)

                self._mouseIsInRegion = False
                # self.Refresh()
                event.Skip()
                return

        if not regionContainsPoint:
            if self._mouseIsInRegion:  # Update Visual.
                self._mouseIsInRegion = False
                self.Refresh()
            self._mouseAction = None
            if self.GetToolTip():  # Only show the tooltip when in region, not when in rect.
                self.GetToolTip().Enable(False)

            # Pass the wx.EVT_MOTION to the parent
            selfPosX, selfPosY = self.GetPosition()
            underX, underY = selfPosX + x, selfPosY + y
            self.SendMouseEvent(parent, wx.wxEVT_MOTION, underX, underY)

            for child in self.GetChildren():
                if child.IsMousePositionInRegion():
                    child._mouseAction = HOVER
                    child._mouseIsInRegion = True
                else:
                    child._mouseAction = None
                    child._mouseIsInRegion = False
                child.Refresh()

        else:
            if self.HasCapture():
                self._mouseAction = CLICK
            else:
                self._mouseAction = HOVER
                if self.GetToolTip(): # HOVER event happens before CLICK.
                    self.GetToolTip().Enable(True)
            if hasattr(self.GetParent(), '_sbbChildBmp'):
                parent._mouseAction = None
                parent.Refresh()
            if not self._mouseIsInRegion:
                self._mouseIsInRegion = True
                self.Refresh()

        for sibling in self.GetSBBSiblings():
            if not sibling.IsMousePositionInRegion():
                pass # print(sibling.GetName(), 'isinregion')

        selfIsMousePositionInRegion = self.IsMousePositionInRegion()
        for sibling in self.GetSBBSiblings():
            sibIsMousePositionInRegion = sibling.IsMousePositionInRegion()
            if sibIsMousePositionInRegion and not selfIsMousePositionInRegion:
                sibling._mouseAction = HOVER
                sibling.Refresh()
            else:
                sibling._mouseAction = None
                sibling.Refresh()

        # self.Refresh()


        event.Skip()
        # print('OnMotion (%s, %s)' % (x, y))

    # def OnLeftUp(self, event):
    #     """
    #     Handles the ``wx.EVT_LEFT_UP`` event for :class:`ShapedBitmapButton`.
    #
    #     :param `event`: a :class:`MouseEvent` event to be processed.
    #     """
    #
    #     x, y = event.GetPosition()
    #
    #     parent = self.GetParent()
    #     imAChild = hasattr(parent, '_sbbChildBmp')
    #     if not self._region.Contains(x, y) and imAChild:  # I am a child here.
    #         selfPosX, selfPosY = self.GetPosition()
    #         underX, underY = selfPosX + x, selfPosY + y
    #         # print('selfPos = %s, %s' %(selfPosX, selfPosY))
    #         # print('OnLeftUp x, y = %s,%s' %(x, y))
    #         if parent._region.Contains(underX, underY):
    #             # Send the event back to the parent because we are hovering over it and have clicked.
    #             # self.parent._mouseIsInRegion = True
    #             # parent._mouseAction = HOVER
    #             # parent.Notify()
    #             parent.SendMouseEvent(parent, wx.wxEVT_LEFT_UP, underX, underY)
    #             return
    #
    #     if not self._region.Contains(x, y):  # Pass the wx.EVT_LEFT_UP to the parent
    #         selfPosX, selfPosY = self.GetPosition()
    #         underX, underY = selfPosX + x, selfPosY + y
    #         self.SendMouseEvent(self.parent, wx.wxEVT_LEFT_UP, underX, underY)
    #         return
    #
    #     if not self.IsEnabled() or not self.HasCapture():
    #         return
    #
    #     if self.HasCapture():
    #         self.ReleaseMouse()
    #
    #     if self._region.Contains(x, y):
    #         self._mouseAction = HOVER
    #         self.Notify()
    #     else:
    #         self._mouseAction = None
    #
    #     self.Refresh()
    #     event.Skip()

# __main__ Demo -------------------------------------------------------------


if __name__ == '__main__':
    import wx
    from wx.lib.embeddedimage import PyEmbeddedImage

    seamless = PyEmbeddedImage(
        "iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAAAAABWESUoAAAAIElEQVR4AWP4DwVnoACdP1IU"
        "oEug80eIgtH0MJoekPkA0wuWLp08mZwAAAAASUVORK5CYII=")

    shapedbitmapbutton_normal = PyEmbeddedImage(
        "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"
        "SUVORK5CYII=")

    shapedbitmapbutton_hover = PyEmbeddedImage(
        "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")

    shapedbitmapbutton_pressed = PyEmbeddedImage(
        "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")


    class ShapedBitmapButtonFrame(wx.Frame):
        def __init__(self, parent):
            wx.Frame.__init__(self, parent, -1, "ShapedBitmapButton Demo")

            vbSizer = wx.BoxSizer(wx.VERTICAL)
            vbSizer.Add(ShapedBitmapButtonPanel(self), 1, wx.EXPAND | wx.ALL, 25)
            self.SetSizer(vbSizer)
            self.Fit()
            statusBar = self.CreateStatusBar()
            import sys
            pyVER = '%d.%d.%d %s' % sys.version_info[:4]
            verInfo = 'wxPython %s running on Python %s' % (wx.version(), pyVER)
            statusBar.SetStatusText(verInfo, 0)


    class ShapedBitmapButtonPanel(wx.Panel):
        def __init__(self, parent):
            wx.Panel.__init__(self, parent, -1, style=wx.BORDER_SIMPLE)

            self.backgroundBitmap = backgroundBitmap = MakeDisplaySizeBackgroundBitmap(seamless.GetBitmap())

            hbSizer = wx.GridSizer(rows=2, cols=3, vgap=15, hgap=15)

            myNormalBmp = shapedbitmapbutton_normal.GetBitmap()
            myPressedBmp = shapedbitmapbutton_pressed.GetBitmap()
            myHoverBmp = shapedbitmapbutton_hover.GetBitmap()
            myDisabledBmp = shapedbitmapbutton_normal.GetBitmap().ConvertToDisabled()

            for i in range(5):
                sButton = ShapedBitmapButton(self, -1,
                    bitmap=myNormalBmp,
                    pressedBmp=myPressedBmp,
                    hoverBmp=myHoverBmp,
                    disabledBmp=myDisabledBmp,
                    parentBgBmp=backgroundBitmap,
                    label='Undo', labelForeColour=wx.WHITE,
                    labelRotation=27.0, labelPosition=(2, 14),
                    labelFont=wx.Font(11, wx.FONTFAMILY_DEFAULT,
                                         wx.FONTSTYLE_NORMAL,
                                         wx.FONTWEIGHT_BOLD),
                    style=wx.BORDER_SIMPLE  # Show the Rect
                        )

                if i == 1:
                    if hasattr(wx.Image, 'Rotate180'):
                        sButton.Rotate180()
                        sButton.SetLabel('Redo')
                        sButton.SetLabelPosition((20, 22))
                if i == 2:
                    sButton.SetLabelEnabled(False)
                    ttStr = ('I have a ToolTip!\n'
                             'Enter/Return Key fires me off also\n'
                             'because I have style=wx.WANTS_CHARS')
                    sButton.SetToolTip(wx.ToolTip(ttStr))
                    sButton.SetWindowStyle(wx.WANTS_CHARS)  # Don't Eat Enter/Return Key
                if i == 3:
                    sButton.Mirror()
                    sButton.SetLabelEnabled(False)
                if i == 4:
                    sButton.SetLabel('New')

                sButton.Bind(wx.EVT_BUTTON, self.OnButton)
                sButton.Bind(wx.EVT_RIGHT_UP, self.OnRightUp)
                hbSizer.Add(sButton, 0, wx.ALIGN_CENTER | wx.ALL, 15)

            sButton.timer = wx.Timer(sButton)
            sButton.Bind(wx.EVT_TIMER, self.OnTimer)
            sButton.timer.Start(500)  # Every half a second.

            # Lets make a rotated button too.
            sButton = ShapedBitmapButton(self, -1,
                bitmap=shapedbitmapbutton_normal.GetImage().Rotate90().ConvertToBitmap(),
                pressedBmp=shapedbitmapbutton_pressed.GetImage().Rotate90().ConvertToBitmap(),
                hoverBmp=shapedbitmapbutton_hover.GetImage().Rotate90().ConvertToBitmap(),
                parentBgBmp=backgroundBitmap,
                style=wx.BORDER_SIMPLE  # Show the Rect
                    )
            sButton.Bind(wx.EVT_BUTTON, self.OnButton)
            sButton.Bind(wx.EVT_RIGHT_UP, self.OnRightUp)
            hbSizer.Add(sButton, 0, wx.ALIGN_CENTER | wx.ALL, 15)


            self.SetSizer(hbSizer)
            self.Fit()

            self.Bind(wx.EVT_PAINT, self.OnPaint)
            self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)

        ## Additionally reduce OnSize bg bmp flicker of the buttons while resizing. ####
            self.Bind(wx.EVT_SIZE, self.OnSize)                                     #
            self.SetDoubleBuffered(True)                                            #
                                                                                    #
        def OnSize(self, event):                                                    #
            self.Layout()                                                           #
        ################################################################################

        def OnTimer(self, event):
            evtObj = event.GetEventObject()
            evtObj.SetLabelEnabled(not evtObj.GetLabelEnabled())
            evtObj.Refresh()

        def OnRightUp(self, event):
            print('OnRightUp')

        def OnButton(self, event):
            print('wxPython Rocks!')

        def OnEraseBackground(self, event):
            pass

        def OnPaint(self, event):
            dc = wx.BufferedPaintDC(self)
            dc.Clear()
            dc.DrawBitmap(self.backgroundBitmap, 0, 0, True)


    class ShapedBitmapButtonApp(wx.App):
        def OnInit(self):
            gMainWin = ShapedBitmapButtonFrame(None)
            gMainWin.SetTitle('ShapedBitmapButton Demo')
            gMainWin.Show()

            return True


    gApp = ShapedBitmapButtonApp(redirect=False,
            filename=None,
            useBestVisual=False,
            clearSigInt=True)

    gApp.MainLoop()

