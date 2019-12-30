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

from wx.lib.embeddedimage import PyEmbeddedImage

# Optimized pngs.
COLORBAR = PyEmbeddedImage(
    "iVBORw0KGgoAAAANSUhEUgAABfoAAAABCAIAAAAJjIjyAAAAJ0lEQVR4Ae3CAREAAAiEMOwf"
    "+g0Cu92Aa6WHdAsn3Y7W+WilYa3wA94A/SDDQ0HPAAAAAElFTkSuQmCC")

COLORBARGRADIENT = PyEmbeddedImage(
    "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"
    "4AM5c+YuPAv46QCuUj9gwNQPGHCx9wEDbhUTYMDzw0H3X34KpGpP5/mOWq7lIdX8/yr1g1SN"
    "+lUDWex9kKq1+lE1kPP9Efe/jBEjRk4cssceMWKkSv1GjFC/ESPV3jdihC86R4zMd/+xWxeq"
    "1ixJE4bJ+/3d3XXc3d3d3d3d3e0ahsYGGGCds/Prid3Eg6xVXZUVGdGQL30H9hfUd9SrX8zW"
    "tevVq69Cv3r10K9efTX31avvRIN69fObh8f+eLFixflv/usXK1ZchX7FiqFfseJi7itWjAWK"
    "W4vn1w+D/feqcl/MqlCLkUpW7ouF8v6r0M+qUNAvFKvF3GdVqFZKCsXq/Oqhsn9Rdk8FCRK8"
    "wzBty/KCBAkeVVXoJ0gQ+gkSrOY+QYKdUCBIcH551O0mKV92txr++V+MUbJsL8U//1Xo559/"
    "6Oef/2ru889/J3r4539+sWB/uoZtthPf/Pkattne11Shn222oZ9ttqu5zzbbnTBim+35+VG0"
    "n6GNiEYpEY1OGbLbBRrl3Xr/VeiHfo2gH/o1KuY+7mvUyjjo12h+tmD/BQsk9SoW3/yRggAn"
    "Ggq8CuiHfujHu6oCSYu5j/uStvIO+iWdnx4VifnL69Onv5utxWlanz79KvTTpw/99OlXc58+"
    "/U400Kc/P1mxf38abK211ru53J9qrXXstAr9WmsN/VprXc19rbXuxIHWWs+Pj+PFVMVO9xfF"
    "YXgxUslThsXZG65CvzgMQz/D4hRzXxyGW0nKsDjzo+NsMeUXvuiii4sRv+5FF108TqrQ76KL"
    "0O+ii9Xcd9FFyOi86OL8cMf+/NHwz3/mmz9/tLjIP/9N6OGff+jnn/9q7vPPfyd6+Od/fnCc"
    "xUcw44E99vKjubjCHnsLD1XoZ4896GePvWrus8deJx3YY2++/2DZ78pcyIAroVF2JY9SV6rQ"
    "D/2uQD/0u1LMfdx3pRUK0O/KfO8G+0+bvHwLLbRYjNdm7PIttNCiCv1aaAH9WmhRzH0ttGhl"
    "gRZazHcX7L/4vn37iwG69r59+1Xot28f+u3br+a+ffudCLBvf75zHAQGLiBOnHjgm/9+ihMn"
    "XoV+4sShnzjxYu4TJ95KCuLE59sr9ivOAk9x7pt/X6w42VFxFfqhXzH0Q7/iYu7jvmKAaEW/"
    "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")


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


## def getColorBarAswxImage():
##     """
##     Get a colorbar as a wx.Image
##
##     :rtype: A `wx.Image`
##     """
##     colorBarData = generateColorBar()
##     img = wx.Image(1530, 1)
##     for i, color in enumerate(colorBarData, 0):
##         img.SetRGB(x=i, y=0,
##                    r=color[0],
##                    g=color[1],
##                    b=color[2])
##     return img

def getColorBar(getAswxBitmap=True):
    if getAswxBitmap:
        return COLORBAR.GetBitmap()
    return COLORBAR.GetImage()


## def getColorBarGradientAswxImage():
##     """
##     Get a colorbar gradient as a wx.Image
##
##     :rtype: A `wx.Image`
##     """
##     colorBarData = generateColorBar()
##     bmp = wx.Bitmap(1530, 512)
##     dc = wx.MemoryDC(bmp)
##     for i, color in enumerate(colorBarData, 0):
##         dc.GradientFillLinear(rect=wx.Rect(x=i, y=0, width=1, height=256),
##                               initialColour=wx.Colour(color[0],
##                                                       color[1],
##                                                       color[2],
##                                                       color[3]),
##                               destColour=wx.WHITE,
##                               nDirection=wx.TOP)
##         dc.GradientFillLinear(rect=wx.Rect(x=i, y=256, width=1, height=256),
##                               initialColour=wx.Colour(color[0],
##                                                       color[1],
##                                                       color[2],
##                                                       color[3]),
##                               destColour=wx.BLACK,
##                               nDirection=wx.BOTTOM)
##     bmp = dc.GetAsBitmap()
##     del dc
##     img = bmp.ConvertToImage()
##     return img

def getColorBarGradient(getAswxBitmap=True):
    if getAswxBitmap:
        return COLORBARGRADIENT.GetBitmap()
    return COLORBARGRADIENT.GetImage()


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
    GetRed, GetGreen, GetBlue = tmpImg.GetRed, tmpImg.GetGreen, tmpImg.GetBlue
    gradientColors = [(GetRed(x=i, y=0),
                       GetGreen(x=i, y=0),
                       GetBlue(x=i, y=0),
                       255)
                            for i in range(0, 256, 1)]

    bmp = wx.Bitmap(256, 256)
    dc = wx.MemoryDC(bmp)
    # Loop optimizations.
    wxRect = wx.Rect
    wxColour = wx.Colour
    wxBLACK = wx.BLACK
    wxBOTTOM = wx.BOTTOM
    dc_GradientFillLinear = dc.GradientFillLinear
    # for i, gradcolor in enumerate(gradientColors, 0):
    #     dc_GradientFillLinear(rect=wxRect(x=i, y=0, width=1, height=256),
    #                           initialColour=wxColour(gradcolor[0],
    #                                                  gradcolor[1],
    #                                                  gradcolor[2],
    #                                                  gradcolor[3]),
    #                           destColour=wxBLACK,
    #                           nDirection=wxBOTTOM)
    [dc_GradientFillLinear(rect=wxRect(x=i, y=0, width=1, height=256),
                           initialColour=wxColour(gradcolor[0],
                                                  gradcolor[1],
                                                  gradcolor[2],
                                                  gradcolor[3]),
                           destColour=wxBLACK,
                           nDirection=wxBOTTOM)
        for i, gradcolor in enumerate(gradientColors, 0)]

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
    # Loop optimizations.
    wxRect = wx.Rect
    wxColour = wx.Colour
    wxBOTTOM = wx.BOTTOM

    bmp = wx.Bitmap(256, 1)
    dc = wx.MemoryDC(bmp)
    dc.GradientFillLinear(rect=wxRect(x=0, y=0, width=256, height=1),
                          initialColour=wxColour(color1[0],
                                                  color1[1],
                                                  color1[2],
                                                  color1[3]),
                          destColour=wxColour(color2[0],
                                               color2[1],
                                               color2[2],
                                               color2[3]),
                          nDirection=wx.RIGHT)
    tmpImg = dc.GetAsBitmap().ConvertToImage()
    del dc
    GetRed, GetGreen, GetBlue = tmpImg.GetRed, tmpImg.GetGreen, tmpImg.GetBlue
    gradientColors1 = [(GetRed(x=i, y=0),
                        GetGreen(x=i, y=0),
                        GetBlue(x=i, y=0),
                        255)
                            for i in range(0, 256, 1)]
    #---
    bmp = wx.Bitmap(256, 1)
    dc = wx.MemoryDC(bmp)
    dc.GradientFillLinear(rect=wxRect(x=0, y=0, width=256, height=1),
                          initialColour=wxColour(color3[0],
                                                  color3[1],
                                                  color3[2],
                                                  color3[3]),
                          destColour=wxColour(color4[0],
                                               color4[1],
                                               color4[2],
                                               color4[3]),
                          nDirection=wx.RIGHT)
    tmpImg = dc.GetAsBitmap().ConvertToImage()
    del dc
    GetRed, GetGreen, GetBlue = tmpImg.GetRed, tmpImg.GetGreen, tmpImg.GetBlue
    gradientColors2 = [(GetRed(x=i, y=0),
                        GetGreen(x=i, y=0),
                        GetBlue(x=i, y=0),
                        255)
                            for i in range(0, 256, 1)]
    #---
    bmp = wx.Bitmap(256, 256)
    dc = wx.MemoryDC(bmp)
    dc_GradientFillLinear = dc.GradientFillLinear
    for i, gradcolor in enumerate(gradientColors1, 0):
        dc_GradientFillLinear(rect=wxRect(x=i, y=0, width=1, height=256),
                              initialColour=wxColour(gradcolor[0],
                                                      gradcolor[1],
                                                      gradcolor[2],
                                                      gradcolor[3]),
                              destColour=wxColour(gradientColors2[i][0],
                                                   gradientColors2[i][1],
                                                   gradientColors2[i][2],
                                                   gradientColors2[i][3]),
                              nDirection=wxBOTTOM)

    bmp = dc.GetAsBitmap()
    del dc
    img = bmp.ConvertToImage()
    return img


if __name__ == '__main__':
    #-----------------------------
    # Export image for optimizing before re-embedding.
    ## img = getColorBarAswxImage()
    ## img.SaveFile('colorbar.png', wx.BITMAP_TYPE_PNG)
    ##
    ## img = getColorBarGradientAswxImage()
    ## img.SaveFile('colorbargradient.png', wx.BITMAP_TYPE_PNG)
    #-----------------------------

    import sys

    class MyFrame(wx.Frame):
        def __init__(self, parent):
            wx.Frame.__init__(self, parent, wx.ID_ANY, "Coloring Demo")

            wxVER = 'wxPython %s' % wx.version()
            pyVER = 'python %d.%d.%d.%s' % sys.version_info[0:4]
            versionInfos = '%s %s' % (wxVER, pyVER)
            self.CreateStatusBar().SetStatusText(versionInfos)

            notebook = wx.Notebook(self, wx.ID_ANY)
            bmp = getColorBar()
            staticbitmap = wx.StaticBitmap(notebook, wx.ID_ANY, bmp)
            notebook.AddPage(staticbitmap, "ColorBar")

            bmp = getColorBarGradient()
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

