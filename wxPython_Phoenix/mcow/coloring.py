#!/usr/bin/env python
# -*- coding: utf-8 -*-

# -------------------------------------------------------------------------- #
# (c) Edward Greig, @ 25 Jun 2019 - coloring
# Latest Revision: Edward Greig @ 25 Jun 2019, 21.00 GMT
#
# For All Kind Of Problems, Requests Of Enhancements And Bug Reports, Please
# Write To Me At:
#
# metaliobovinus@gmail.com
#
# Or, Obviously, To The wxPython Mailing List!!!
#
# -------------------------------------------------------------------------- #

"""
coloring
========

various functions to make colorbars for pickers, selectors, painters, and
other stuff.


License And Version
-------------------

coloring is distributed under the wxPython license.

Edward Greig, @ 25 Jun 2019
Latest revision: Edward Greig @ 25 Jun 2019, 21.00 GMT

Version 0.1

"""

#-Imports----------------------------------------------------------------------

#--wxPython Imports.
import wx


def generateColorBar():
    """
    Get a list of rgba color tuples to create a colorbar

    :rtype: list
    """
    r = 255
    g = 0
    b = 0
    a = 255
    colorBar = []
    # Start at Red (255, 0, 0) and go to Yellow (255, 255, 0)
    for i in range(0, 256, 1):
        g = i
        colorBar.append((r, g, b, a))
    # Start at Yellow (255, 255, 0) and go to Green (0, 255, 0)
    for i in reversed(range(0, 256, 1)):
        r = i
        colorBar.append((r, g, b, a))
    # Start at Green (0, 255, 0) and go to Cyan (0, 255, 255)
    for i in range(0, 256, 1):
        b = i
        colorBar.append((r, g, b, a))
    # Start at Cyan (0, 255, 255) and go to Blue (0, 0, 255)
    for i in reversed(range(0, 256, 1)):
        g = i
        colorBar.append((r, g, b, a))
    # Start at Blue (0, 0, 255) and go to Magenta (255, 0, 255)
    for i in range(0, 256, 1):
        r = i
        colorBar.append((r, g, b, a))
    # Start at Magenta (255, 0, 255) and go to Red (255, 0, 0)
    for i in reversed(range(0, 256, 1)):
        b = i
        colorBar.append((r, g, b, a))

    # Remove the duplicates while preserving the order.
    colorBar = list(sorted(set(colorBar), key=colorBar.index))
    assert len(colorBar) == 1530
    return colorBar


def getColorBarAsPILImage():
    """
    Get a colorbar as a PIL.Image

    :rtype: A `PIL.Image`
    """
    colorBarData = generateColorBar()
    from PIL import Image
    img = Image.new(mode='RGBA', size=(1530, 1), color=0)
    img.putdata(data=colorBarData, scale=1.0, offset=0.0)
    return img


def getColorBarAswxImage():
    """
    Get a colorbar as a wx.Image

    :rtype: A `wx.Image`
    """
    colorBarData = generateColorBar()
    img = wx.Image(1530, 1)
    for i, color in enumerate(colorBarData, 0):
        img.SetRGB(x=i, y=0,
                   r=color[0],
                   g=color[1],
                   b=color[2])
    return img


def getColorBarGradientAswxImage():
    """
    Get a colorbar gradient as a wx.Image

    :rtype: A `wx.Image`
    """
    colorBarData = generateColorBar()
    bmp = wx.Bitmap(1530, 512)
    dc = wx.MemoryDC(bmp)
    for i, color in enumerate(colorBarData, 0):
        dc.GradientFillLinear(rect=wx.Rect(x=i, y=0, width=1, height=256),
                              initialColour=wx.Colour(color[0],
                                                      color[1],
                                                      color[2],
                                                      color[3]),
                              destColour=wx.WHITE,
                              nDirection=wx.TOP)
        dc.GradientFillLinear(rect=wx.Rect(x=i, y=256, width=1, height=256),
                              initialColour=wx.Colour(color[0],
                                                      color[1],
                                                      color[2],
                                                      color[3]),
                              destColour=wx.BLACK,
                              nDirection=wx.BOTTOM)
    bmp = dc.GetAsBitmap()
    del dc
    img = bmp.ConvertToImage()
    return img


def makeColorBarSquaredGradientAswxImage(color=(255, 0, 0, 255)):
    """
    Get a colorbar squared gradient as a wx.Image

    :param `color`: A rgba tuple
    :type `color`: `tuple
    :rtype: A `wx.Image`
    """
    bmp = wx.Bitmap(256, 1)
    dc = wx.MemoryDC(bmp)
    dc.GradientFillLinear(rect=wx.Rect(x=0, y=0, width=256, height=1),
                          initialColour=wx.Colour(color[0],
                                                  color[1],
                                                  color[2],
                                                  color[3]),
                          destColour=wx.WHITE,
                          nDirection=wx.LEFT)
    tmpImg = dc.GetAsBitmap().ConvertToImage()
    del dc
    gradientColors = [(tmpImg.GetRed(x=i, y=0),
                       tmpImg.GetGreen(x=i, y=0),
                       tmpImg.GetBlue(x=i, y=0),
                       255)
                            for i in range(0, 256, 1)]

    bmp = wx.Bitmap(256, 256)
    dc = wx.MemoryDC(bmp)
    for i, gradcolor in enumerate(gradientColors, 0):
        dc.GradientFillLinear(rect=wx.Rect(x=i, y=0, width=1, height=256),
                              initialColour=wx.Colour(gradcolor[0],
                                                      gradcolor[1],
                                                      gradcolor[2],
                                                      gradcolor[3]),
                              destColour=wx.BLACK,
                              nDirection=wx.BOTTOM)

    bmp = dc.GetAsBitmap()
    del dc
    img = bmp.ConvertToImage()
    return img


def makeSquaredGradientAswxImage(color1=(255, 0, 0, 255),
                                 color2=(255, 255, 0, 255),
                                 color3=(0, 0, 255, 255),
                                 color4=(0, 255, 0, 255)):
    """
    Get a colorbar squared gradient as a wx.Image

    :param `color1`: A rgba tuple
    :type `color1`: `tuple
    :param `color2`: A rgba tuple
    :type `color2`: `tuple
    :param `color3`: A rgba tuple
    :type `color3`: `tuple
    :param `color4`: A rgba tuple
    :type `color4`: `tuple
    :rtype: A `wx.Image`
    """
    bmp = wx.Bitmap(256, 1)
    dc = wx.MemoryDC(bmp)
    dc.GradientFillLinear(rect=wx.Rect(x=0, y=0, width=256, height=1),
                          initialColour=wx.Colour(color1[0],
                                                  color1[1],
                                                  color1[2],
                                                  color1[3]),
                          destColour=wx.Colour(color2[0],
                                               color2[1],
                                               color2[2],
                                               color2[3]),
                          nDirection=wx.RIGHT)
    tmpImg = dc.GetAsBitmap().ConvertToImage()
    del dc
    gradientColors1 = [(tmpImg.GetRed(x=i, y=0),
                        tmpImg.GetGreen(x=i, y=0),
                        tmpImg.GetBlue(x=i, y=0),
                        255)
                            for i in range(0, 256, 1)]
    #---
    bmp = wx.Bitmap(256, 1)
    dc = wx.MemoryDC(bmp)
    dc.GradientFillLinear(rect=wx.Rect(x=0, y=0, width=256, height=1),
                          initialColour=wx.Colour(color3[0],
                                                  color3[1],
                                                  color3[2],
                                                  color3[3]),
                          destColour=wx.Colour(color4[0],
                                               color4[1],
                                               color4[2],
                                               color4[3]),
                          nDirection=wx.RIGHT)
    tmpImg = dc.GetAsBitmap().ConvertToImage()
    del dc
    gradientColors2 = [(tmpImg.GetRed(x=i, y=0),
                        tmpImg.GetGreen(x=i, y=0),
                        tmpImg.GetBlue(x=i, y=0),
                        255)
                            for i in range(0, 256, 1)]
    #---
    bmp = wx.Bitmap(256, 256)
    dc = wx.MemoryDC(bmp)
    for i, gradcolor in enumerate(gradientColors1, 0):
        dc.GradientFillLinear(rect=wx.Rect(x=i, y=0, width=1, height=256),
                              initialColour=wx.Colour(gradcolor[0],
                                                      gradcolor[1],
                                                      gradcolor[2],
                                                      gradcolor[3]),
                              destColour=wx.Colour(gradientColors2[i][0],
                                                   gradientColors2[i][1],
                                                   gradientColors2[i][2],
                                                   gradientColors2[i][3]),
                              nDirection=wx.BOTTOM)

    bmp = dc.GetAsBitmap()
    del dc
    img = bmp.ConvertToImage()
    return img


if __name__ == '__main__':
    import sys

    class MyFrame(wx.Frame):
        def __init__(self, parent):
            wx.Frame.__init__(self, parent, wx.ID_ANY, "Coloring Demo")

            wxVER = 'wxPython %s' % wx.version()
            pyVER = 'python %d.%d.%d.%s' % sys.version_info[0:4]
            versionInfos = '%s %s' % (wxVER, pyVER)
            self.CreateStatusBar().SetStatusText(versionInfos)

            notebook = wx.Notebook(self, wx.ID_ANY)
            bmp = getColorBarAswxImage().ConvertToBitmap()
            staticbitmap = wx.StaticBitmap(notebook, wx.ID_ANY, bmp)
            notebook.AddPage(staticbitmap, "ColorBar")

            bmp = getColorBarGradientAswxImage().ConvertToBitmap()
            staticbitmap = wx.StaticBitmap(notebook, wx.ID_ANY, bmp)
            notebook.AddPage(staticbitmap, "ColorBarGradient")

            bmp = makeColorBarSquaredGradientAswxImage().ConvertToBitmap()
            staticbitmap = wx.StaticBitmap(notebook, wx.ID_ANY, bmp)
            notebook.AddPage(staticbitmap, "ColorBarSquaredGradient")

            bmp = makeSquaredGradientAswxImage().ConvertToBitmap()
            staticbitmap = wx.StaticBitmap(notebook, wx.ID_ANY, bmp)
            notebook.AddPage(staticbitmap, "SquaredGradient")

            vbSizer = wx.BoxSizer(wx.VERTICAL)
            vbSizer.Add(notebook, 1, wx.EXPAND)
            self.SetSizer(vbSizer)

    app = wx.App(0)

    frame = MyFrame(None)
    app.SetTopWindow(frame)
    frame.Show()

    app.MainLoop()
