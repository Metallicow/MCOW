#!/usr/bin/env python

# --------------------------------------------------------------------------------- #
# THREEWAYSPLITTER wxPython IMPLEMENTATION
#
# (c) Andrea Gavana, @ 03 Nov 2006 - FourWaySplitter
# (c) Edward Greig, @ 13 Jan 2014 - ThreeWaySplitter
# Latest Revision: Edward Greig @ 20 May 2014, 21.00 GMT
#
#
# TODO List
#
# 0. Any ideas?
# 1. Ability to define custom brush/pen for the splitter sashes, so custom
#    looking sashes are easy to achieve.
# 2. AnimTo... Center, LeftCenter, RightCenter, TopCenter, BottomCenter
# 3. i18n the PopupMenu Labels(wx.GetTranslation).
#    Is _(u'label text') right? I don't think Phoenix is officially supporting
#    python 3.0-3.2, so this should be fine I'm guessing...
# 4. Figure out a Mixin for Three/Four WaySplitters determining if a the
#    brother/sister splitter widgets are a child and provide extra Way splitter
#    functionality for adjusting them both/all at the same time.
# 5. A optional small bitmap 4-16px or so(user setable also) to draw on
#    the splitter crossroads for extra style points.
# 6. Optional/Setable Snapping to edge option if not MinSize.
#    Ex: when splitter is within say 10 px of the edge, then snap to edge.
# 7. Remove all obsolete stuff/code from phoenix version, since project Phoenix
#    aims to progress and not be backwards compatible.
#    ummm...??? wx.VERSION, _RENDER_VER
# 8. Optional animating the splitters when sending them wherever....
#    ...To a particular point in the ThreeWaySplitter
#    Similar to AUI SmoothDocking effects.
# 9. optimize, Optimize, OPTIMIZE!
#
# IDEAS List
#
# 1. Maybe a Blender-style optional right click merge(adjust window size programmatically)
#    screen drawing with thingy arrows. Sorta like AUI Dock Guides popup.
# 2. Similar to blender also, maybe a Dynamic Sash Type Mixin to allow duplicating
#    of one of the windows.
#
# For All Kind Of Problems, Requests Of Enhancements And Bug Reports, Please
# Write To Us At:
#
# andrea.gavana@maerskoil.com
# andrea.gavana@gmail.com
#
# metaliobovinus@gmail.com
#
# Or, Obviously, To The wxPython Mailing List!!!
#
#
# End Of Comments
# --------------------------------------------------------------------------------- #

"""
:class:`ThreeWaySplitter` is a layout manager which manages 3 children like 3 panes in a
window. It was initially developed with SourceCoder for the SourceCoder Library.
It is very similar to it's parent/(brother/sister) widget `FourWaySplitter` from
the AGW package as that was the base starting point.


Description
===========

The :class:`ThreeWaySplitter` is a layout manager which manages three children like three
panes in a window.

The :class:`ThreeWaySplitter` allows interactive repartitioning of the panes by
means of moving the central splitter bars. When the :class:`ThreeWaySplitter` is itself
resized, each child is proportionally resized, maintaining the same split-percentage.

The main characteristics of :class:`ThreeWaySplitter` are:

- Handles horizontal, vertical or three way sizing via the sashes;
- Delayed or live update when resizing;
- Possibility to swap windows;
- Setting the vertical and horizontal split fractions;
- Possibility to expand a window by hiding the other 2.

And a lot more. See the demo for a complete review of the functionalities.


Usage
=====

Usage example::

    import wx
    import wx.lib.mcow.threewaysplitter as tws

    class MyFrame(wx.Frame):

        def __init__(self, parent):

            wx.Frame.__init__(self, parent, -1, "ThreeWaySplitter Demo")

            splitter = tws.ThreeWaySplitter(self, -1, agwStyle=wx.SP_LIVE_UPDATE)

            # Put in some coloured panels...
            for colour in [wx.RED, wx.WHITE, wx.BLUE]:

                panel = wx.Panel(splitter)
                panel.SetBackgroundColour(colour)

                splitter.AppendWindow(panel)


    # our normal wxApp-derived class, as usual

    app = wx.App(0)

    frame = MyFrame(None)
    app.SetTopWindow(frame)
    frame.Show()

    app.MainLoop()



Supported Platforms
===================

:class:`ThreeWaySplitter` has been tested on the following platforms:
  * Windows (Windows XP);
  * Linux Ubuntu (Dapper 6.06)


Window Styles
=============

This class supports the following window styles:

================== =========== ==================================================
Window Styles      Hex Value   Description
================== =========== ==================================================
``SP_NOSASH``             0x10 No sash will be drawn on :class:`ThreeWaySplitter`.
``SP_LIVE_UPDATE``        0x80 Don't draw XOR line but resize the child windows immediately.
``SP_3DBORDER``          0x200 Draws a 3D effect border.
================== =========== ==================================================


Events Processing
=================

This class processes the following events:

================================== ==================================================
Event Name                         Description
================================== ==================================================
``EVT_SPLITTER_SASH_POS_CHANGED``  The sash position was changed. This event is generated after the user releases the mouse after dragging the splitter. Processes a ``wx.wxEVT_COMMAND_SPLITTER_SASH_POS_CHANGED`` event.
``EVT_SPLITTER_SASH_POS_CHANGING`` The sash position is in the process of being changed. You may prevent this change from happening by calling `Veto` or you may also modify the position of the tracking bar to properly reflect the position that would be set if the drag were to be completed at this point. Processes a ``wx.wxEVT_COMMAND_SPLITTER_SASH_POS_CHANGING`` event.
================================== ==================================================


License And Version
===================

:class:`ThreeWaySplitter` is distributed under the wxPython license.

(c) Andrea Gavana, @ 03 Nov 2006 - FourWaySplitter
(c) Edward Greig, @ 13 Jan 2014 - ThreeWaySplitter
Latest Revision: Edward Greig @ 20 May 2014, 21.00 GMT

Version 0.5

"""

__docformat__ = "ReST"


import wx
from wx.lib.embeddedimage import PyEmbeddedImage
## print('wxPython %s' % wx.version())

# Define a Translation function.
_ = wx.GetTranslation

_RENDER_VER = (2,6,1,1)

# Tolerance for mouse shape and sizing
_TOLERANCE = 5

# Modes
NOWHERE = 0
""" No sashes are changing position. """
FLAG_CHANGED = 1
""" Sashes are changing position. """
FLAG_PRESSED = 2
""" Sashes are in a pressed state. """

# ThreeWaySplitter styles
SP_NOSASH = wx.SP_NOSASH
""" No sash will be drawn on :class:`ThreeWaySplitter`. """
SP_LIVE_UPDATE = wx.SP_LIVE_UPDATE
""" Don't draw XOR line but resize the child windows immediately. """
SP_3DBORDER = wx.SP_3DBORDER
""" Draws a 3D effect border. """

# ThreeWaySplitter events
EVT_SPLITTER_SASH_POS_CHANGING = wx.EVT_SPLITTER_SASH_POS_CHANGING
""" The sash position is in the process of being changed. You may prevent this change""" \
""" from happening by calling `Veto` or you may also modify the position of the tracking""" \
""" bar to properly reflect the position that would be set if the drag were to be""" \
""" completed at this point. Processes a ``wx.wxEVT_COMMAND_SPLITTER_SASH_POS_CHANGING`` event."""
EVT_SPLITTER_SASH_POS_CHANGED = wx.EVT_SPLITTER_SASH_POS_CHANGED
""" The sash position was changed. This event is generated after the user releases the""" \
""" mouse after dragging the splitter. Processes a ``wx.wxEVT_COMMAND_SPLITTER_SASH_POS_CHANGED`` event. """

# ThreeWaySplitter context menu optimized png images
tws_full_1_16 = PyEmbeddedImage(
    "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAIAAACQkWg2AAAABnRSTlMAAAAAAABupgeRAAAA"
    "4UlEQVR4AZWSQW7DMAwEFaE/6xfSB+SSf/TmL4vcXZaUHNgBUiAZDilifeDF7VMu27aRFAnS"
    "AbivaWaeM2vYqC0ZmX1J/L7fWxSSInJliybNSYrS+nBpv7dbp9QOIq1Kci5WOjG3TlAnYpai"
    "JinmdgSCeSehJ1hViAs9AsAcHVDsqPolpCbu1gGPM1LallEGKWrlmBegBZc83MNCU4fvF6SH"
    "cVKaXUiUBKA7IPI/n1kX3IMKvZRKuZRI1gV3nYkoDzjdgbObob0NhMv152rD5r+23pGbj+Hw"
    "XJLM4EA10/Ypf8vkR+52p0r/AAAAAElFTkSuQmCC")
#----------------------------------------------------------------------
tws_full_2_16 = PyEmbeddedImage(
    "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAIAAACQkWg2AAAABnRSTlMAAAAAAABupgeRAAAA"
    "50lEQVR4AZWSUY7DMAhEHSv36iXaC/Qq/cmVDTOw4FCtu9qq6vOEOBAzIkpvX7Idx0HSSJAK"
    "QPWMIqIRYw0ZuQtG5HYz3i+XOOpFi2Ve0C3wlMc798djp1l74nXz5XQoMlUKw07QFyy1tK1k"
    "O0sQ7SSqaC31Bk6JYgdsGpYzW/m8ehrdoqIqHdBy+A+WCkwHuKfDPLJ0b9mz+tRH2hQ6HT7B"
    "ZwTQFahp3c9YskUBk+mg+q4rVmWCTAetoZOM9bT41BWCchepoWvSX9qfxwCG7Xq7ypD5r533"
    "ETsdQ6GxCSIHBfJiqH3LD+vWT3Eyd00AAAAAAElFTkSuQmCC")
#----------------------------------------------------------------------
tws_full_3_16 = PyEmbeddedImage(
    "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAIAAACQkWg2AAAABnRSTlMAAAAAAABupgeRAAAA"
    "40lEQVR4AZWSS07EMBBEG4uLseICwwWQuAYbNrmy3fXBTkdKpBHAvFTKlZbiWtjxKE/btpEU"
    "CTIBZJaPMXL6fProK036nD1LfPl4DYdtSRGxvLJDlGSJsiP89f7ZKMUP2OHzY2kWNoKWT6Sp"
    "3Xwkr1SOkY2E11BXHVAnXBqJBsjhE8UuXXSslDJHA1L3cOk+Y2+AL2jn2saaSCElshr+hNUD"
    "oCUQDk8pzOm+SKXjF1ZD/tqAQwVXQ6bpJcnWeRhrWNufjmQbA/43EJ5ub7fRx37Xau0zZe+J"
    "mbPuHxJYL6fiUb4BsIBZS/ELK1MAAAAASUVORK5CYII=")
#----------------------------------------------------------------------
tws_loneside_bottom_16 = PyEmbeddedImage(
    "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAIAAACQkWg2AAAABnRSTlMAAAAAAABupgeRAAAA"
    "rklEQVR4AZWPMQ7CQAwEr/AP4B9Q5xMp00ELDyHKl29nfSABouGK3BS2tNLI3jJKbNuWmS3T"
    "mdiGz5QECFFVAUmqEmVdH88ey7L8h9M0RbZWegD/oVCkc79gEZnuC+pecNgDL4HCpiuoJxiH"
    "7a4A6oQmbK6Xq9AbpPrZdp7OJypCgJBxRJTb/fbczeF4CEPZTdrBiGAyJA8IzYE1zzOSUP2W"
    "hloxEr+6NnamWxnlBajaHws2BrBaAAAAAElFTkSuQmCC")
#----------------------------------------------------------------------
tws_loneside_bottom_swap_1_2_16 = PyEmbeddedImage(
    "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAIAAACQkWg2AAAABnRSTlMAAAAAAABupgeRAAAB"
    "H0lEQVR4AZWRTUoEUQyEM9K3GhS8g+7cCgLOGdwO6CFczvHUXad+4stjRhB74wddCU0qxSPx"
    "X3bH41GSJUogCUxFZmIoEmuu3Q3WTCy2Hm9v5UYuWRBNvby/n06n+M1+v7/q0Rq02p1VLlYB"
    "iD8kchE1d4dsqmH7uGlgYukByQ5abZhKGbmZwIW0bM7154aCvJkA5DBAtqwfIJHMLQM7YVCW"
    "7GmjSwMbyI0EYnc4PH9+fCWy6bJeap8AreeD9PoByKe316qoxuXW/qyosF0drVEj6uHmeiFA"
    "aY67hxy+UHM4zn1vEbkAINAGN6XzJWd/mZWmwYSWTO7Imokxo2LujnJY/cceWo1p7u7u73Kd"
    "b8asQxJYVxDdXJ7L/kQq/ss3WSn1HuPJ/BYAAAAASUVORK5CYII=")
#----------------------------------------------------------------------
tws_loneside_bottom_swap_1_3_16 = PyEmbeddedImage(
    "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAIAAACQkWg2AAAABnRSTlMAAAAAAABupgeRAAAB"
    "IElEQVR4AZWQsU6DMQyE3SiCp4KnKFIH1K4sDLBUqniASjDysvHdOTiJykI78MWx71fOSvwX"
    "+yf1fD5LCokSSAIruzsy52rehkqaO2qETqeT/WG32719HwGEJIpgLfVjf6yKsGsAEBURmpH0"
    "kMOLqFsNmXv6EAI12+moEq83OJRwLgXJUjYOFvLmk0KhjAVHAF5J2DUcg+UTSNDlnDfwxg2+"
    "6dbHEJlGva93ICqJw/7g8EmWtiqp9+0rGlIDIxOsCciXr8/erQ8iV187ZN3m30yprGb9+fGh"
    "EqA07TFMYXGhT/P6Xk8TWQEQGA3rQIp5NvXFK82GIFTcuSENNMlSRNi0TiETjSO6lMHgZvu0"
    "9TZnxqotFVoDkeJ3XI6tDPsvP2UD0of26GMzAAAAAElFTkSuQmCC")
#----------------------------------------------------------------------
tws_loneside_bottom_swap_2_3_16 = PyEmbeddedImage(
    "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAIAAACQkWg2AAAABnRSTlMAAAAAAABupgeRAAAB"
    "E0lEQVR4AZWQS07DMBRF08iCBZQNdQ9lygypSHTAqBMkpl0AC+gSgZnf/Rg/R5k3R859VqJ7"
    "FLtMGynX61WSJUogCSwZEeiJQI2au06NQLH1ejjIidxkQTT1dbt9fF8AWCkjWOby+XKZZbt1"
    "Mm3Jam5sDYCotORKGhWIeX07yeYiUw4A/Y/TAwvUqDMwSxxeU8rlrFBGYBQXg0maCrCQTvei"
    "XzapMwBrqBYozTMQhYQ8Pq1AIhlIxPX6wFD0LOw0p3zU6KaODcSuTeMyeuR8LA8gdufz++/P"
    "XyCSHHWdCFRkBpCZ+lKm09up3c3+aV8ITHcjsmBLgVCJ4IaCuTs+H6OOM2PMHgHUCiI363GZ"
    "j0hNW/kHtf36FbCOQ3UAAAAASUVORK5CYII=")
#----------------------------------------------------------------------
tws_loneside_left_16 = PyEmbeddedImage(
    "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAA00lEQVR4AaWTwWnEUAxEh+Vf"
    "Nh24gWwPbsJXN5QFd+LekhTwZ0ZWTAx7swDvg4duYiShlpl4h7YsS0YEtl3vyoal//r7/YP7"
    "xx2SQBHqRJcgEmTfFfB8fuUZ8zxnxTiO2WLbcAZJVFDELRxFA6HCFFqEiwYdFZTR7OsjSMTN"
    "VjljhY8ExQhd2C8BSYc8KiVIhCy0OkHHuq44YxgGNBUJ1IWKI4Gu7yBsNBUNJKHCCjTS16+w"
    "GU0mpmk6HkREp16PYhmPxyf42j5hGbZ2A+ENyMy3/ANI4zaPfy0AWAAAAABJRU5ErkJggg==")
#----------------------------------------------------------------------
tws_loneside_left_swap_1_2_16 = PyEmbeddedImage(
    "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAIAAACQkWg2AAAABnRSTlMAAAAAAABupgeRAAAB"
    "KElEQVR4AZWQPU4DMRCFzWqbcINcgByEgyBRRPTQIoHSpKCihoIudwMOsO9nzNiLQqSEIp9n"
    "nlw8+409lDMZt9ut7bBlUxKZ+v35tbhckESuCVPbJRPAMcLX67UkW5ENJR/PTy83d46GozpM"
    "K+TbzWZ0NEqtWUkprQD8uS2FczECxGC57olZDXB2K0xbmpUCB1slPeHITukAkzuSmoYl0hXU"
    "KEVJcpjoEWn370jN56QplSUSY2oc0lNAMLqxiejKnqWeoHn49JUIK7fGxMe3d87gQMSjhMQG"
    "p91uV45YLpcjpZIRbhGtaiScWE7RE0jZsad/GIhyCksDyWr3i3tIP0yeThA9ALqopT/7j/8S"
    "FBopvD7cEwAxZaeAolarK4AJCFFqbSvKufwATwIPa8TB1hwAAAAASUVORK5CYII=")
#----------------------------------------------------------------------
tws_loneside_left_swap_1_3_16 = PyEmbeddedImage(
    "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAIAAACQkWg2AAAABnRSTlMAAAAAAABupgeRAAAB"
    "HklEQVR4AZWPMU4DUQxEP9JvwpVSIjoOkIoGkQqqcADoUiIq2pwPOMB6Zrx4dqMoUpIib73W"
    "NPbzb9fSt9utpJQogSRQ/e/nd3G7qBj1DTE4FUMEeqbu1muSEj0WLHYf77vvXTthuVx2pWnj"
    "WFW05oqIdo4SdlHjgZy7St3OwUCXWLszbZKbqXMvGNjJdKxjclJ47uJJQHQSeYxkA84PcDJw"
    "Pt5PzxQrKgasVivMxFEjTgyFFBhePzdTLlKUA/R0/9hBtlLICpdNiQH785giNQWQkwGglAdq"
    "QH7DtFmiDJP0hMgOYJSmxW6VbQDSl1SpcAfpUo/gzdj87CNswH4/qfka2VIGxtfbBhGBGOqv"
    "FiD48vBcoQgEQfr3be1a/gFMgPqVjrcK8gAAAABJRU5ErkJggg==")
#----------------------------------------------------------------------
tws_loneside_left_swap_2_3_16 = PyEmbeddedImage(
    "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAIAAACQkWg2AAAABnRSTlMAAAAAAABupgeRAAAB"
    "BElEQVR4AZWSMW5UQRQEV1+TmHuRIW28CUggJAKIyFYicrIBAQeAEwIHmFfVbzGeAFt8B66g"
    "NUG3eqY14/BMxuVySdKJCSqgv3/+unlxAxTFrAnUHbOK0Z3z+Xx4zOl0+vrmQ/ov6Ws6xDZv"
    "b2+3dP/fW1X/3NHYabqL2mL2Aiy3HRJdisWWuBeYuUdNYkch18KhT17JjiuWYFCooewEKDrL"
    "biRX1EQc6k5g8uX7Dxb1QOSphvnp2+e+I0k6ppOQdy9fD/YamCx329HcH1Bkk/03PFwpNtoY"
    "HewFgE7n8UyiZKtyv4FEswTFqO3AOh6PVBU1i/XDxI+v3teahhIVTezDc/kDjyqwmPEYu/IA"
    "AAAASUVORK5CYII=")
#----------------------------------------------------------------------
tws_loneside_right_16 = PyEmbeddedImage(
    "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAA0UlEQVR4AaVTQYrDMBATxX1I"
    "XtA95xO55kMt5Cd53vZoSROvSZbe7EAqEMMgELIGp1IKvkFalqVEBLZKV8qGpc98/76R7gkU"
    "oUxkCSJB5koBr9ez9DDPc1Mbx7Gk2Db0QLKtibiF48RATc0UUoRPDHJbk5Hs60+QiJutvoHa"
    "Bj4SGLVpSDrIY3LfCXc6koVkC+u6ooXHz6Op2UaSjR6UdZJA1zuIPcGJQU+3Aon09StsewfE"
    "NE0QCYrI1OejKGdYxjAM/5fhvtuqDIQ3oJTyFf8AW8E2zBBuhaUAAAAASUVORK5CYII=")
#----------------------------------------------------------------------
tws_loneside_right_swap_1_2_16 = PyEmbeddedImage(
    "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAIAAACQkWg2AAAABnRSTlMAAAAAAABupgeRAAAB"
    "HElEQVR4AZWQu04DMRBFTWS6fF6QEtFBh5QPYFuabUD8JqlI6bkPs7alBEFS5Gj2bjPjM3ZO"
    "N5LneZZkiRJIAiOP38d8nwOBEgVALJQIZFvTNKV/7Ha7l493khItMbjw9vyUZV9UR4TtVOtS"
    "Cym1CkQWdWUA9YRHioEs8cpASbXasi15EGAmr660ZFvJXWFbFYhM4vIAwr/pFnYDt9stBnEO"
    "UmN528kWXatANMPnfm9brhJpSYb0OL36DxLJFcjRTQsSORIoaA+qpmjVTAaxIqAOyZbu3aqB"
    "oOQT/cHUDIBsmpQ4DNS4SJX6wV3ShwnlCMK9twWhiu4KxF1N/dpnaN5tHjZRAhGB/l8igFK+"
    "Dof1eo3mCoJsn0ilW/kBSmL5L2HIXUwAAAAASUVORK5CYII=")
#----------------------------------------------------------------------
tws_loneside_right_swap_1_3_16 = PyEmbeddedImage(
    "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAIAAACQkWg2AAAABnRSTlMAAAAAAABupgeRAAAB"
    "JUlEQVR4AZWSPU4DMRBGTWTOE65AAZS5A0DDHZCQaNJASwMFXY5HSn8/s+zYUoIgKfJkj3ZX"
    "M/M81pZTqev12nbYsimJHHH7va3nFQQbGknMNIA1wpcPN+FIsjJEO/T1/PH49irJVraDZl7u"
    "bqsjdtmZL+c7A0BElGkqU1JKLhCLzBi9FaYsmaYEcNoRI1rgwpY73Z5+KjfQ5t7DbscAVJXy"
    "oxWWkzF7FqDMzIeJrsi6iUSVaHp4JEfPtgQifjEs6gZ9Pr1zgH2QPA6fo0dY86MppmGz2ZR/"
    "LC+W8Yc+Z6VUDsHGvFCnIleaohvIcggQsmNHvzCn4UgBycnujbtkDE1XQMcMZ1PpY+9R5AxY"
    "rVYEQDRw/GFsTdT99RVJEKKU21aUU/kBbrUPpmIqvU8AAAAASUVORK5CYII=")
#----------------------------------------------------------------------
tws_loneside_right_swap_2_3_16 = PyEmbeddedImage(
    "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAIAAACQkWg2AAAABnRSTlMAAAAAAABupgeRAAAB"
    "BUlEQVR4AZWSsUpDQRREH2H9kHxHKis/wtoynY2CYJlSULDRIn6hKd+dMxNJFg0h23iKyxYz"
    "zM7lLqZ/0jabje3Y2AKkPnffu3bVSqW5ZklVVXOVWuLru5s4B+w4yA7b54/t13Y6Z7VaLZz8"
    "qe2AE0epqumCUjXjrg4x+PgQVOnSQKnZ9A7GBwgQUTWPEmiQOCa/Blsghl+SqoGsLjQ4AmEo"
    "DQyIBnw+vatTpwEeJKAGelmvkzh7G2I7sm8fHwYJ0ARdfWqRgDRrnIBk+2AwR7UBeT/sYGiS"
    "nJwvyQJJo9JeVKEYuho5AuxhAqGJun99U1Wp5lK/MM0zYrlcSioVAgQ2mf7LD5gssPL4C4lr"
    "AAAAAElFTkSuQmCC")
#----------------------------------------------------------------------
tws_loneside_top_16 = PyEmbeddedImage(
    "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAIAAACQkWg2AAAABnRSTlMAAAAAAABupgeRAAAA"
    "sElEQVR4AZWQTWqAMBSEY+iy3sCTeAyx23oGD1Hxym9+0jbYdtMI5gPfyMAwYVIvw3metost"
    "m5LI6wIgCYKBIAkAATAdx8fnY+Z5zi4lPQZEtvw8IDDb6mlQljqeROJF4va+gahUiV8lGKz3"
    "Zy5R4+uY9n1vDrIsy39zmqbacNPe8CVlSu0A2DDFLHY0uDbcBNDyRWdAdws2AkXD+rYiQAC8"
    "NAAygiLAv0FVP0tOvXwBKRUeppmzP64AAAAASUVORK5CYII=")
#----------------------------------------------------------------------
tws_loneside_top_swap_1_2_16 = PyEmbeddedImage(
    "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAIAAACQkWg2AAAABnRSTlMAAAAAAABupgeRAAAB"
    "FklEQVR4AZWQ0U0kMRBEh9F8QlRHBgsB8AEBkAHiZxMgAE4k6XpVPUfLyx3o2A+eytVuu62S"
    "vC4/ZDsej0kqcYJtmC4JEGJoQPcaEltVfj08LHtTVfv+vs2yL1VpTypV8+Jiebq7W1PlfxBj"
    "LBAeQ0PMIxBjCK1xPnAvMGTKLUsMGVpi7Tnb2HILvkic0EASXu2yPk1MTq1gzFFEO9ps3p6f"
    "hZou46MiBu2CduOry6vN9uvv1+U/DofDy+NjVaX2VIjLub6/74TlO4DTdOxKpaiyvWJ//0Ck"
    "dldI7OlgNnM2IYnj9optsqcTzjwQuOyk5eCATDbJZxJkZ4aQHXfn8sXN7Y2GkMSsQ4IxMBJ/"
    "P9S9Ymf5KX8A9mIBzQZkv6gAAAAASUVORK5CYII=")
#----------------------------------------------------------------------
tws_loneside_top_swap_1_3_16 = PyEmbeddedImage(
    "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAIAAACQkWg2AAAABnRSTlMAAAAAAABupgeRAAAB"
    "G0lEQVR4AZWQMVLDUAxEHY9LcoSchiuEA6TJUHEAOiZNGloaWtocUPtW31j5EyBDmuyspP3f"
    "+y2NhnsxHY/HzGyZzsQ29CwJECIUpRaExNRaPu73w1xorc3zInOYh+W+cv2rtf5hNbztduNy"
    "9C9IYywQjlCIfgUiQmhM5wWuAEN2umiJkKEoxvLZxlbRcEVBhwJJeLSb9cfR0TWC6NaSqphs"
    "vg4HoUKVuFREUFlQ2Xj9sJ5sP7+/9FX0nZil+PP143Q6DdfYbDbV4cddfueiGg0Y/sH2hN3d"
    "zS3tPAtsdOMBZjTkGbarlLviZoesDtRI6YXlr4yNdXMkcpScZB/GF3faoBsPmlfbp61CSKLX"
    "kCACU+KyUFfkwuFefAPj3ROkXV/vkQAAAABJRU5ErkJggg==")
#----------------------------------------------------------------------
tws_loneside_top_swap_2_3_16 = PyEmbeddedImage(
    "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAIAAACQkWg2AAAABnRSTlMAAAAAAABupgeRAAAA"
    "9klEQVR4AZWQsU4CQRiED7KlvBC1j4CtVCRWFpb2EhpLbXzSnflm8X5EtIQv2ZnNZLJzuTbd"
    "yOJwOCQZCYkB+0cl2Zblrl63mS552u/fjlezXq9bxpiuRlYLma4GuSXcskCDGz7JVgNvH7ey"
    "irL+65a7S2WXYlZ3qwY8vT+PjCKZL3g2vl4/P15eKhvHjDgMcr/b1cKlXX1SHQ/b53Zg9soG"
    "0AzntxmBnC4Gy3O7shRU28ZL7JwAyqpdx/YlZATsHFMLdg3+PZUYjGwG/7KKcZYScQIpObcD"
    "ts6TwalZaorF5mGjLkvyyWeR3bux5MsPpU4g0618A/Gt3v6nu6fUAAAAAElFTkSuQmCC")

# RightClick Menu IDs
ID_LONESIDE_LEFT = wx.NewId()
ID_LONESIDE_TOP = wx.NewId()
ID_LONESIDE_RIGHT = wx.NewId()
ID_LONESIDE_BOTTOM = wx.NewId()
ID_LONESIDE_LEFT_SWAP_1_2 = wx.NewId()
ID_LONESIDE_LEFT_SWAP_1_3 = wx.NewId()
ID_LONESIDE_LEFT_SWAP_2_3 = wx.NewId()
ID_LONESIDE_TOP_SWAP_1_2 = wx.NewId()
ID_LONESIDE_TOP_SWAP_1_3 = wx.NewId()
ID_LONESIDE_TOP_SWAP_2_3 = wx.NewId()
ID_LONESIDE_RIGHT_SWAP_1_2 = wx.NewId()
ID_LONESIDE_RIGHT_SWAP_1_3 = wx.NewId()
ID_LONESIDE_RIGHT_SWAP_2_3 = wx.NewId()
ID_LONESIDE_BOTTOM_SWAP_1_2 = wx.NewId()
ID_LONESIDE_BOTTOM_SWAP_1_3 = wx.NewId()
ID_LONESIDE_BOTTOM_SWAP_2_3 = wx.NewId()
ID_CENTER_SPLITTERS_WINDOWS = wx.NewId()

# ---------------------------------------------------------------------------- #
# Class ThreeWaySplitterEvent
# ---------------------------------------------------------------------------- #

class ThreeWaySplitterEvent(wx.PyCommandEvent):
    """
    This event class is almost the same as :class:`SplitterEvent` except
    it adds an accessor for the sash index that is being changed.  The
    same event type IDs and event binders are used as with
    :class:`SplitterEvent`.
    """

    def __init__(self, evtType=wx.wxEVT_NULL, splitter=None):
        """
        Default class constructor.

        :param `evtType`: the event type;
        :param `splitter`: the associated :class:`ThreeWaySplitter` window.
        """

        wx.PyCommandEvent.__init__(self, evtType)

        if splitter:
            self.SetEventObject(splitter)
            self.SetId(splitter.GetId())

        self.sashIdx = -1
        self.sashPos = -1
        self.isAllowed = True


    def SetSashIdx(self, idx):
        """
        Sets the index of the sash currently involved in the event.

        :param `idx`: an integer between 0 and 3, representing the index of the
         sash involved in the event.
        """

        self.sashIdx = idx


    def SetSashPosition(self, pos):
        """
        In the case of ``EVT_SPLITTER_SASH_POS_CHANGED`` events, sets the new sash
        position. In the case of ``EVT_SPLITTER_SASH_POS_CHANGING`` events, sets
        the new tracking bar position so visual feedback during dragging will represent
        that change that will actually take place. Set to -1 from the event handler
        code to prevent repositioning.

        :param `pos`: the new sash position.

        :note: May only be called while processing ``EVT_SPLITTER_SASH_POS_CHANGING``
         and ``EVT_SPLITTER_SASH_POS_CHANGED`` events.
        """

        self.sashPos = pos


    def GetSashIdx(self):
        """ Returns the index of the sash currently involved in the event. """

        return self.sashIdx


    def GetSashPosition(self):
        """
        Returns the new sash position.

        :note: May only be called while processing ``EVT_SPLITTER_SASH_POS_CHANGING``
         and ``EVT_SPLITTER_SASH_POS_CHANGED`` events.
        """

        return self.sashPos


    # methods from wx.NotifyEvent
    def Veto(self):
        """
        Prevents the change announced by this event from happening.

        :note: It is in general a good idea to notify the user about the reasons
         for vetoing the change because otherwise the applications behaviour (which
         just refuses to do what the user wants) might be quite surprising.
        """

        self.isAllowed = False


    def Allow(self):
        """
        This is the opposite of :meth:`~ThreeWaySplitterEvent.Veto`: it explicitly allows the event to be processed.
        For most events it is not necessary to call this method as the events are
        allowed anyhow but some are forbidden by default (this will be mentioned
        in the corresponding event description).
        """

        self.isAllowed = True


    def IsAllowed(self):
        """
        Returns ``True`` if the change is allowed (:meth:`~ThreeWaySplitterEvent.Veto` hasn't been called) or
        ``False`` otherwise (if it was).
        """

        return self.isAllowed


# ---------------------------------------------------------------------------- #
# Class ThreeWaySplitter
# ---------------------------------------------------------------------------- #

class ThreeWaySplitter(wx.Panel):
    """
    This class is very similar to :class:`SplitterWindow` except that it
    allows for three windows and two sashes.  Many of the same styles,
    constants, and methods behave the same as in :class:`SplitterWindow`.
    However, in addition of the ability to drag the vertical and the
    horizontal sash, by dragging at the intersection between the two
    sashes, it is possible to resize the three windows at the same time.

    :note: These things are not yet supported:

     * Using negative sash positions to indicate a position offset from the end;
     * User controlled unsplitting with double clicks on the sash (but supported via the
       :meth:`ThreeWaySplitter.SetExpanded() <ThreeWaySplitter.SetExpanded>` method);
     * Sash gravity.


    """

    def __init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=0, agwStyle=0, loneSide=wx.LEFT,
                 minSplitterSize=(0, 0), name="ThreeWaySplitter"):
        """
        Default class constructor.

        :param `parent`: parent window. Must not be ``None``;
        :param `id`: window identifier. A value of -1 indicates a default value;
        :param `pos`: the control position. A value of (-1, -1) indicates a default position,
         chosen by either the windowing system or wxPython, depending on platform;
        :param `size`: the control size. A value of (-1, -1) indicates a default size,
         chosen by either the windowing system or wxPython, depending on platform;
        :param `style`: the underlying :class:`Panel` window style;
        :param `agwStyle`: the AGW-specific window style. It can be a combination of the
         following bits:

         ================== =========== ==================================================
         Window Styles      Hex Value   Description
         ================== =========== ==================================================
         ``SP_NOSASH``             0x10 No sash will be drawn on :class:`ThreeWaySplitter`.
         ``SP_LIVE_UPDATE``        0x80 Don't draw XOR line but resize the child windows immediately.
         ``SP_3DBORDER``          0x200 Draws a 3D effect border.
         ================== =========== ==================================================

        :param `loneSide`: the lone single(solo) Window opposite of the other two
         will be on one of these sides: wx.LEFT, wx.RIGHT, wx.TOP, wx.BOTTOM.
        :param `name`: the window name.
        """

        # always turn on tab traversal
        style |= wx.TAB_TRAVERSAL

        # and turn off any border styles
        style &= ~wx.BORDER_MASK
        style |= wx.BORDER_NONE

        self._agwStyle = agwStyle
        self._loneSide = loneSide

        # initialize the base class
        wx.Panel.__init__(self, parent, id, pos, size, style, name)
        self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)

        self._windows = []
        self._windowsPopupLabels = ['0', '1', '2']

        self._splitx = 0
        self._splity = 0
        self._expanded = -1
        self._fhor = 5000
        self._fver = 5000
        self._offx = 0
        self._offy = 0
        self._mode = NOWHERE
        self._flags = 0
        self._isHot = False

        self._doubleClickSwitch = True
        self._doubleClickSwitchModifiers = wx.MOD_NONE

        self._sashTrackerPen = wx.Pen(wx.BLACK, 2, wx.PENSTYLE_SOLID)

        self._hSplitMinSizeX = 0
        self._vSplitMinSizeY = 0

        # self._sashCursorWE = wx.Cursor(wx.CURSOR_SIZEWE)
        # self._sashCursorNS = wx.Cursor(wx.CURSOR_SIZENS)
        # self._sashCursorSIZING = wx.Cursor(wx.CURSOR_SIZING)
        self.SetSplitterCursors()
        self._hasCapture = False
        self._hasCaptureMode = NOWHERE

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_MOTION, self.OnMotion)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        self.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)
        self.Bind(wx.EVT_LEAVE_WINDOW, self.OnLeaveWindow)
        self.Bind(wx.EVT_ENTER_WINDOW, self.OnEnterWindow)
        self.Bind(wx.EVT_RIGHT_UP, self.OnRightUp)

        self.Bind(wx.EVT_LEFT_DCLICK, self.OnLeftDClick)

        self.Bind(wx.EVT_MENU, self.SetLoneSideFromPopupMenu, id=ID_LONESIDE_LEFT)
        self.Bind(wx.EVT_MENU, self.SetLoneSideFromPopupMenu, id=ID_LONESIDE_TOP)
        self.Bind(wx.EVT_MENU, self.SetLoneSideFromPopupMenu, id=ID_LONESIDE_RIGHT)
        self.Bind(wx.EVT_MENU, self.SetLoneSideFromPopupMenu, id=ID_LONESIDE_BOTTOM)
        self.Bind(wx.EVT_MENU, self.Swap1and2, id=ID_LONESIDE_LEFT_SWAP_1_2)
        self.Bind(wx.EVT_MENU, self.Swap1and3, id=ID_LONESIDE_LEFT_SWAP_1_3)
        self.Bind(wx.EVT_MENU, self.Swap2and3, id=ID_LONESIDE_LEFT_SWAP_2_3)
        self.Bind(wx.EVT_MENU, self.Swap1and2, id=ID_LONESIDE_TOP_SWAP_1_2)
        self.Bind(wx.EVT_MENU, self.Swap1and3, id=ID_LONESIDE_TOP_SWAP_1_3)
        self.Bind(wx.EVT_MENU, self.Swap2and3, id=ID_LONESIDE_TOP_SWAP_2_3)
        self.Bind(wx.EVT_MENU, self.Swap1and2, id=ID_LONESIDE_RIGHT_SWAP_1_2)
        self.Bind(wx.EVT_MENU, self.Swap1and3, id=ID_LONESIDE_RIGHT_SWAP_1_3)
        self.Bind(wx.EVT_MENU, self.Swap2and3, id=ID_LONESIDE_RIGHT_SWAP_2_3)
        self.Bind(wx.EVT_MENU, self.Swap1and2, id=ID_LONESIDE_BOTTOM_SWAP_1_2)
        self.Bind(wx.EVT_MENU, self.Swap1and3, id=ID_LONESIDE_BOTTOM_SWAP_1_3)
        self.Bind(wx.EVT_MENU, self.Swap2and3, id=ID_LONESIDE_BOTTOM_SWAP_2_3)
        self.Bind(wx.EVT_MENU, self.CenterSplittersWindows, id=ID_CENTER_SPLITTERS_WINDOWS)

        self.SetSplitterMinSize(minSplitterSize[0], minSplitterSize[1])


    def SavePerspective(self):
        """
        Save a perspectiveStr to be used later with :meth:`LoadPerspective`.

        :return: The perspective string to save.
        :rtype: str
        """
        opt1 = 'loneside=%s' % self._loneSide
        opt2 = 'hsplitminsizex=%s' % self._hSplitMinSizeX
        opt3 = 'vsplitminsizey=%s' % self._vSplitMinSizeY
        opt4 = 'splitx=%s' % self._splitx
        opt5 = 'splity=%s' % self._splity
        opt6 = 'expanded=%s' % self._expanded
        opt7 = 'fhor=%s' % self._fhor
        opt8 = 'fver=%s' % self._fver
        opt9 = 'offx=%s' % self._offx
        opt10 = 'offy=%s' % self._offy

        perspectiveStr = ';'.join([opt1, opt2, opt3, opt4, opt5, opt6, opt7, opt8, opt9, opt10])

        return perspectiveStr


    def LoadPerspective(self, perspectiveStr):
        """
        Load a perspectiveStr previously saved with :meth:`SavePerspective`.

        :param `perspectiveStr`: The perspective string to load.
        :type `perspectiveStr`: str
        """
        optsList = perspectiveStr.split(';')
        for opt in optsList:
            if 'loneside=' in opt:
                self._loneSide = int(opt[len('loneside='):])
            elif 'hsplitminsizex=' in opt:
                self._hSplitMinSizeX = int(opt[len('hsplitminsizex='):])
            elif 'vsplitminsizey=' in opt:
                self._vSplitMinSizeY = int(opt[len('vsplitminsizey='):])
            elif 'splitx=' in opt:
                # print('DEBUG TWS LoadPerspective')
                # print(opt[len('splitx='):])
                self._splitx = float(opt[len('splitx='):])
                # self._splitx = int(opt[len('splitx='):])
            elif 'splity=' in opt:
                self._splity = float(opt[len('splity='):])
                # self._splity = int(opt[len('splity='):])
            elif 'expanded=' in opt:
                self._expanded = int(opt[len('expanded='):])
            elif 'fhor=' in opt:
                self._fhor = int(opt[len('fhor='):])
            elif 'fver=' in opt:
                self._fver = int(opt[len('fver='):])
            elif 'offx=' in opt:
                self._offx = int(opt[len('offx='):])
            elif 'offy=' in opt:
                self._offy = int(opt[len('offy='):])
            else:
                raise Exception('Unknown opt: %s' % opt)

        self._SizeWindows()


    def SetSplitterCursors(self, cursorBOTH=None,
                                 cursorHORIZONTAL=None,
                                 cursorVERTICAL=None):
        """
        Set the cursors to display for when the mouse is at the direction
        portions of the splitter. Cursors default to system cursors.

        :param `cursorBOTH`: An instance of :class:`Cursor`.
        :param `cursorHORIZONTAL`: An instance of :class:`Cursor`.
        :param `cursorVERTICAL`: An instance of :class:`Cursor`.
        """
        if cursorBOTH is None:
            cursorBOTH = wx.Cursor(wx.CURSOR_SIZING)
        if cursorHORIZONTAL is None:
            cursorHORIZONTAL = wx.Cursor(wx.CURSOR_SIZEWE)
        if cursorVERTICAL is None:
            cursorVERTICAL = wx.Cursor(wx.CURSOR_SIZENS)
        self._sashCursorSIZING = cursorBOTH
        self._sashCursorWE = cursorHORIZONTAL
        self._sashCursorNS = cursorVERTICAL


    def GetLoneSide(self):
        return self._loneSide


    def GetMinimumSizeX(self):
        return self._hSplitMinSizeX


    def SetMinimumSizeX(self, minimumSizeX=0):
        self._hSplitMinSizeX = minimumSizeX
        self._SizeWindows()


    def GetMinimumSizeY(self):
        return self._vSplitMinSizeY


    def SetMinimumSizeY(self, minimumSizeY=0):
        self._vSplitMinSizeY = minimumSizeY
        self._SizeWindows()


    def SetSplitterMinSize(self, minimumSizeX=0, minimumSizeY=0):
        self._hSplitMinSizeX = minimumSizeX
        self._vSplitMinSizeY = minimumSizeY
        self._SizeWindows()


    def OnLeftDClick(self, event):
        """
        Handles the ``wx.EVT_LEFT_DCLICK`` event for :class:`ThreeWaySplitter`.

        :param `event`: a :class:`MouseEvent` event to be processed.
        """
        ## if PHOENIX:
        ##     ms = wx.GetMouseState()
        ##     ctrlDown = ms.ControlDown()
        ##     shiftDown = ms.ShiftDown()
        ##     altDown = ms.AltDown()
        ## else:
        ##     ctrlDown = event.ControlDown()
        ##     shiftDown = event.ShiftDown()
        ##     altDown = event.AltDown()

        # print('event.GetModifiers() = %s' % event.GetModifiers())
        # print('event.ControlDown() = %s' % event.ControlDown())
        # print('event.ShiftDown() = %s' %  event.ShiftDown())
        # print('event.AltDown() = %s' %  event.AltDown())

        if (self._doubleClickSwitch and
                event.GetModifiers() == self._doubleClickSwitchModifiers):
            evtPos = event.GetPosition()
            mode = self.GetMode(evtPos)
            self.DoubleClickSwitch(mode, evtPos)


    def SetSashTrackerPen(self, pen=None):
        """
        Sets the current pen for the DC.

        :param `pen`:
        :type `pen`: :class:`Pen`
        """
        if not pen:
            pen = wx.Pen(wx.BLACK, 2, wx.PENSTYLE_SOLID)
        self._sashTrackerPen = pen


    def SetDoubleClickSwitchModifiers(self, modifiers=0):
        """
        :param `modifiers`: The combination of modifier bit mask's of all pressed modifier keys needed
         to be true for :meth:`DoubleClickSwitch`. 0 or wx.MOD_NONE to unset all modifiers.

        """
        self._doubleClickSwitchModifiers = modifiers


    def DoubleClickSwitch(self, mode, evtPos):
        """
        Do the double click switching.

        :param `mode`: The mode. What determins what the mouse cursor is.
        :param `evtPos`: one of `wx.EVT_MOUSEBTN_DCLICK` event.Position
        """

        width, height = self.GetSize()
        barSize = self._GetSashSize()
        border = self._GetBorderSize()
        totw = width - barSize - 2 * border
        toth = height - barSize - 2 * border
        halfTotalWidth = totw/2
        halfTotalHeight = toth/2

        if mode == wx.BOTH: # Rotate the loneSide
            if self._loneSide == wx.LEFT:
                self.SetLoneSide(wx.TOP)
            elif self._loneSide == wx.TOP:
                self.SetLoneSide(wx.RIGHT)
            elif self._loneSide == wx.RIGHT:
                self.SetLoneSide(wx.BOTTOM)
            elif self._loneSide == wx.BOTTOM:
                self.SetLoneSide(wx.LEFT)
        elif mode == wx.VERTICAL:
            if self._loneSide == wx.LEFT:
                if evtPos[1] < halfTotalHeight: # isToTheTop
                    self.Swap1and2()
                else:
                    self.Swap1and3()
            elif self._loneSide == wx.TOP:
                self.Swap2and3()
            elif self._loneSide == wx.RIGHT:
                if evtPos[1] < halfTotalHeight: # isToTheTop
                    self.Swap1and3()
                else:
                    self.Swap1and2()
            elif self._loneSide == wx.BOTTOM:
                self.Swap2and3()
        elif mode == wx.HORIZONTAL:
            if self._loneSide == wx.LEFT:
                self.Swap2and3()
            elif self._loneSide == wx.TOP:
                if evtPos[0] < halfTotalWidth: # isToTheLeft
                    self.Swap1and3()
                else:
                    self.Swap1and2()
            elif self._loneSide == wx.RIGHT:
                self.Swap2and3()
            elif self._loneSide == wx.BOTTOM:
                if evtPos[0] < halfTotalWidth: # isToTheLeft
                    self.Swap1and2()
                else:
                    self.Swap1and3()


    def EnableDoubleClickSwitch(self, enable=True):
        self._doubleClickSwitch = enable


    def AnimatedMove(self, splitterAnimDirection, frameSpeed=50):
        """
        Animate the splitter moving to a direction.
        """
        width, height = self.GetSize()
        barSize = self._GetSashSize()
        border = self._GetBorderSize()
        totw = width - barSize - 2 * border
        toth = height - barSize - 2 * border
        sad = splitterAnimDirection
        # Standard directions
        if sad == wx.LEFT or sad == wx.WEST:
            while self._fhor > self._hSplitMinSizeX:
                self.SetHSplit(self._fhor - frameSpeed)
                self.Update()
        elif sad == wx.TOP or sad == wx.NORTH:
            while self._fver > self._vSplitMinSizeY:
                self.SetVSplit(self._fver - frameSpeed)
                self.Update()
        elif sad == wx.RIGHT or sad == wx.EAST:
            while self._splitx < totw - self._hSplitMinSizeX:
                self.SetHSplit(self._fhor + frameSpeed)
                self.Update()
        elif sad == wx.BOTTOM or sad == wx.SOUTH:
            while self._splity < toth - self._vSplitMinSizeY:
                self.SetVSplit(self._fver + frameSpeed)
                self.Update()
        # Diagonal directions
        elif sad == wx.TOP | wx.LEFT or sad == wx.NORTH | wx.WEST:
            while self._fver > self._vSplitMinSizeY or self._fhor > self._hSplitMinSizeX:
                self.SetVSplit(self._fver - frameSpeed)
                self.SetHSplit(self._fhor - frameSpeed)
                self.Update()
        elif sad == wx.TOP | wx.RIGHT or sad == wx.NORTH | wx.EAST:
            while self._fver > self._vSplitMinSizeY or self._splitx < totw - self._hSplitMinSizeX:
                self.SetVSplit(self._fver - frameSpeed)
                self.SetHSplit(self._fhor + frameSpeed)
                self.Update()
        elif sad == wx.BOTTOM | wx.LEFT or sad == wx.SOUTH | wx.WEST:
            while self._splity < toth - self._vSplitMinSizeY or self._fhor > self._hSplitMinSizeX:
                self.SetVSplit(self._fver + frameSpeed)
                self.SetHSplit(self._fhor - frameSpeed)
                self.Update()
        elif sad == wx.BOTTOM | wx.RIGHT or sad == wx.SOUTH | wx.EAST:
            while self._splity < toth - self._vSplitMinSizeY or self._splitx < totw - self._hSplitMinSizeX:
                self.SetVSplit(self._fver + frameSpeed)
                self.SetHSplit(self._fhor + frameSpeed)
                self.Update()

        else:
            raise Exception('Incorrect direction. Use one of (wx.LEFT, wx.TOP, wx.RIGHT, or wx.BOTTOM)')


    def SetWindowsPopupLabels(self, window0PopupLabel='1',
                                    window1PopupLabel='2',
                                    window2PopupLabel='3'):
        self._windowsPopupLabels = [window0PopupLabel, window1PopupLabel, window2PopupLabel]


    def OnRightUp(self, event):
        """
        Handles the ``wx.EVT_RIGHT_UP`` event for :class:`ThreeWaySplitter`.
        This pop's up the built-in switcher context menu.

        :param `event`: a :class:`MouseEvent` event to be processed.
        """
        m = wx.Menu()

        winL1 = self._windowsPopupLabels[0]
        winL2 = self._windowsPopupLabels[1]
        winL3 = self._windowsPopupLabels[2]

        swp12Lbl = u'%s' %(' ' + _(u'Swap') + ' ' + winL1 + ' && ' + winL2)
        swp13Lbl = u'%s' %(' ' + _(u'Swap') + ' ' + winL1 + ' && ' + winL3)
        swp23Lbl = u'%s' %(' ' + _(u'Swap') + ' ' + winL2 + ' && ' + winL3)

        # Depending on the loneSide, swap label positions to make the images
        # and the menu labels be on their "right" respective sides, so as not to
        # cause user delayed reversed confusion via reading/eye coordination,
        # since the windows will be behind the popup menu and the user will
        # most likely be able to see them. Left to Right and Top to Bottom.
        if self._loneSide == wx.TOP:
            swp23Lbl = u'%s' %(' ' + _(u'Swap') + ' ' + winL3 + ' && ' + winL2)
        elif self._loneSide == wx.BOTTOM:
            swp12Lbl = u'%s' %(' ' + _(u'Swap') + ' ' + winL2 + ' && ' + winL1)
            swp13Lbl = u'%s' %(' ' + _(u'Swap') + ' ' + winL3 + ' && ' + winL1)
        elif self._loneSide == wx.RIGHT:
            swp12Lbl = u'%s' %(' ' + _(u'Swap') + ' ' + winL2 + ' && ' + winL1)
            swp13Lbl = u'%s' %(' ' + _(u'Swap') + ' ' + winL3 + ' && ' + winL1)
            swp23Lbl = u'%s' %(' ' + _(u'Swap') + ' ' + winL3 + ' && ' + winL2)

        mi = wx.MenuItem()
        mi = wx.MenuItem(m, ID_LONESIDE_LEFT, ' ' + _(u'Left'))
        mi.SetBitmap(tws_loneside_left_16.GetBitmap())
        m.Append(mi)
        mi = wx.MenuItem(m, ID_LONESIDE_TOP, ' ' + _(u'Top'))
        mi.SetBitmap(tws_loneside_top_16.GetBitmap())
        m.Append(mi)
        mi = wx.MenuItem(m, ID_LONESIDE_RIGHT, ' ' + _(u'Right'))
        mi.SetBitmap(tws_loneside_right_16.GetBitmap())
        m.Append(mi)
        mi = wx.MenuItem(m, ID_LONESIDE_BOTTOM, ' ' + _(u'Bottom'))
        mi.SetBitmap(tws_loneside_bottom_16.GetBitmap())
        m.Append(mi)
        m.AppendSeparator()
        if self._loneSide == wx.LEFT:
            mi = wx.MenuItem(m, ID_LONESIDE_LEFT_SWAP_1_2, swp12Lbl, swp12Lbl)
            mi.SetBitmap(tws_loneside_left_swap_1_2_16.GetBitmap())
            m.Append(mi)
            mi = wx.MenuItem(m, ID_LONESIDE_LEFT_SWAP_1_3, swp13Lbl, swp13Lbl)
            mi.SetBitmap(tws_loneside_left_swap_1_3_16.GetBitmap())
            m.Append(mi)
            mi = wx.MenuItem(m, ID_LONESIDE_LEFT_SWAP_2_3, swp23Lbl, swp23Lbl)
            mi.SetBitmap(tws_loneside_left_swap_2_3_16.GetBitmap())
            m.Append(mi)
        elif self._loneSide == wx.TOP:
            mi = wx.MenuItem(m, ID_LONESIDE_TOP_SWAP_1_2, swp12Lbl, swp12Lbl)
            mi.SetBitmap(tws_loneside_top_swap_1_2_16.GetBitmap())
            m.Append(mi)
            mi = wx.MenuItem(m, ID_LONESIDE_TOP_SWAP_1_3, swp13Lbl, swp13Lbl)
            mi.SetBitmap(tws_loneside_top_swap_1_3_16.GetBitmap())
            m.Append(mi)
            mi = wx.MenuItem(m, ID_LONESIDE_TOP_SWAP_2_3, swp23Lbl, swp23Lbl)
            mi.SetBitmap(tws_loneside_top_swap_2_3_16.GetBitmap())
            m.Append(mi)
        elif self._loneSide == wx.RIGHT:
            mi = wx.MenuItem(m, ID_LONESIDE_RIGHT_SWAP_1_2, swp12Lbl, swp12Lbl)
            mi.SetBitmap(tws_loneside_right_swap_1_2_16.GetBitmap())
            m.Append(mi)
            mi = wx.MenuItem(m, ID_LONESIDE_RIGHT_SWAP_1_3, swp13Lbl, swp13Lbl)
            mi.SetBitmap(tws_loneside_right_swap_1_3_16.GetBitmap())
            m.Append(mi)
            mi = wx.MenuItem(m, ID_LONESIDE_RIGHT_SWAP_2_3, swp23Lbl, swp23Lbl)
            mi.SetBitmap(tws_loneside_right_swap_2_3_16.GetBitmap())
            m.Append(mi)
        elif self._loneSide == wx.BOTTOM:
            mi = wx.MenuItem(m, ID_LONESIDE_BOTTOM_SWAP_1_2, swp12Lbl, swp12Lbl)
            mi.SetBitmap(tws_loneside_bottom_swap_1_2_16.GetBitmap())
            m.Append(mi)
            mi = wx.MenuItem(m, ID_LONESIDE_BOTTOM_SWAP_1_3, swp13Lbl, swp13Lbl)
            mi.SetBitmap(tws_loneside_bottom_swap_1_3_16.GetBitmap())
            m.Append(mi)
            mi = wx.MenuItem(m, ID_LONESIDE_BOTTOM_SWAP_2_3, swp23Lbl, swp23Lbl)
            mi.SetBitmap(tws_loneside_bottom_swap_2_3_16.GetBitmap())
            m.Append(mi)

        m.AppendSeparator()
        mi = wx.MenuItem(m, ID_CENTER_SPLITTERS_WINDOWS, ' ' + _(u'Center Splitters/Windows'))
        m.Append(mi)

        self.PopupMenu(m)
        m.Destroy()


    def CenterSplittersWindows(self, event=None):
        """
        Centers the splitters crossroads.
        """
        self._fhor = 5000
        self._fver = 5000
        self._SizeWindows()


    def SetLoneSideFromPopupMenu(self, event):
        """
        Figures out the loneSide to set from the built-in
        popup context menu's id.
        """
        evtId = event.GetId()
        if evtId == ID_LONESIDE_LEFT:
            self.SetLoneSide(wx.LEFT)
        elif evtId == ID_LONESIDE_TOP:
            self.SetLoneSide(wx.TOP)
        elif evtId == ID_LONESIDE_RIGHT:
            self.SetLoneSide(wx.RIGHT)
        elif evtId == ID_LONESIDE_BOTTOM:
            self.SetLoneSide(wx.BOTTOM)


    def Swap1and2(self, event=None):
        """
        Swap(ExchangeWindows) window 1 and window 2.
        """
        win1 = self.GetWindow(0)
        win2 = self.GetWindow(1)
        self.ExchangeWindows(win1, win2)


    def Swap1and3(self, event=None):
        """
        Swap(ExchangeWindows) window 1 and window 3.
        """
        win1 = self.GetWindow(0)
        win3 = self.GetWindow(2)
        self.ExchangeWindows(win1, win3)


    def Swap2and3(self, event=None):
        """
        Swap(ExchangeWindows) window 2 and window 3.
        """
        win2 = self.GetWindow(1)
        win3 = self.GetWindow(2)
        self.ExchangeWindows(win2, win3)


    def SetAGWWindowStyleFlag(self, agwStyle):
        """
        Sets the :class:`ThreeWaySplitter` window style flags.

        :param `agwStyle`: the AGW-specific window style. This can be a combination of the
         following bits:

         ================== =========== ==================================================
         Window Styles      Hex Value   Description
         ================== =========== ==================================================
         ``SP_NOSASH``             0x10 No sash will be drawn on :class:`ThreeWaySplitter`.
         ``SP_LIVE_UPDATE``        0x80 Don't draw XOR line but resize the child windows immediately.
         ``SP_3DBORDER``          0x200 Draws a 3D effect border.
         ================== =========== ==================================================
        """

        self._agwStyle = agwStyle
        self.Refresh()


    def GetAGWWindowStyleFlag(self):
        """
        Returns the :class:`ThreeWaySplitter` window style.

        :see: :meth:`~ThreeWaySplitter.SetAGWWindowStyleFlag` for a list of possible window styles.
        """

        return self._agwStyle


    def AppendWindow(self, window):
        """
        Add a new window to the splitter at the right side or bottom
        of the window stack.

        :param `window`: an instance of :class:`Window`.
        """

        self.InsertWindow(len(self._windows), window)


    def InsertWindow(self, idx, window, sashPos=-1):
        """
        Insert a new window into the splitter at the position given in `idx`.

        :param `idx`: the index at which the window will be inserted;
        :param `window`: an instance of :class:`Window`;
        :param `sashPos`: the sash position after the window insertion.
        """

        assert window not in self._windows, "A window can only be in the splitter once!"

        self._windows.insert(idx, window)

        self._SizeWindows()


    def DetachWindow(self, window):
        """
        Removes the window from the stack of windows managed by the splitter. The
        window will still exist so you should `Hide` or `Destroy` it as needed.

        :param `window`: an instance of :class:`Window`.
        """

        assert window in self._windows, "Unknown window!"

        idx = self._windows.index(window)
        del self._windows[idx]

        self._SizeWindows()


    def ReplaceWindow(self, oldWindow, newWindow):
        """
        Replaces `oldWindow` (which is currently being managed by the
        splitter) with `newWindow`.  The `oldWindow` window will still
        exist so you should `Hide` or `Destroy` it as needed.

        :param `oldWindow`: an instance of :class:`Window`;
        :param `newWindow`: another instance of :class:`Window`.
        """

        assert oldWindow in self._windows, "Unknown window!"

        idx = self._windows.index(oldWindow)
        self._windows[idx] = newWindow

        self._SizeWindows()


    def ExchangeWindows(self, window1, window2):
        """
        Trade the positions in the splitter of the two windows.

        :param `window1`: an instance of :class:`Window`;
        :param `window2`: another instance of :class:`Window`.
        """

        assert window1 in self._windows, "Unknown window!"
        assert window2 in self._windows, "Unknown window!"

        idx1 = self._windows.index(window1)
        idx2 = self._windows.index(window2)
        self._windows[idx1] = window2
        self._windows[idx2] = window1

        win1Lbl = self._windowsPopupLabels[idx1]
        win2Lbl = self._windowsPopupLabels[idx2]
        self._windowsPopupLabels[idx1], self._windowsPopupLabels[idx2] = win2Lbl, win1Lbl

        if "__WXMSW__" in wx.Platform:
            self.Freeze()

        self._SizeWindows()

        if "__WXMSW__" in wx.Platform:
            self.Thaw()


    def GetWindow(self, idx):
        """
        Returns the window at the index `idx`.

        :param `idx`: the index at which the window is located.
        """

        if len(self._windows) > idx:
            return self._windows[idx]

        return None

    # Get top left child
    def GetTopLeft(self):
        """ Returns the top left window (window index: 0). """

        return self.GetWindow(0)


    # Get top right child
    def GetTopRight(self):
        """ Returns the top right window (window index: 1). """

        return self.GetWindow(1)


    # Get bottom left child
    def GetBottomLeft(self):
        """ Returns the bottom left window (window index: 2). """

        return self.GetWindow(2)


    # Get bottom right child
    def GetBottomRight(self):
        """ Returns the bottom right window (window index: 3). """

        return self.GetWindow(3)


    def DoGetBestSize(self):
        """
        Gets the size which best suits the window: for a control, it would be the
        minimal size which doesn't truncate the control, for a panel - the same size
        as it would have after a call to `Fit()`.

        :note: Overridden from :class:`Panel`.
        """

        if not self._windows:
            # something is better than nothing...
            return wx.Size(10, 10)

        width = height = 0
        border = self._GetBorderSize()

        tl = self.GetTopLeft()
        tr = self.GetTopRight()
        bl = self.GetBottomLeft()
        ##4Way## br = self.GetBottomRight()

        for win in self._windows:
            w, h = win.GetEffectiveMinSize()
            width += w
            height += h

        if tl and tr:
          width += self._GetSashSize()

        ##4Way## if bl and br:
        elif bl: # 3Way
          height += self._GetSashSize()

        return wx.Size(width+2*border, height+2*border)


    def SetLoneSide(self, side):
        """
        Sets the loneSide the lone window will be at.

        :param `side`: one of wx.LEFT, wx.TOP, wx.RIGHT, wx.BOTTOM.
        """
        self._loneSide = side
        self.Refresh()
        self.SendSizeEvent() # Need to force a layout refresh.


    # Recompute layout
    def _SizeWindows(self):
        """
        Recalculate the layout based on split positions and split fractions.

        :see: :meth:`~ThreeWaySplitter.SetHSplit` and :meth:`~ThreeWaySplitter.SetVSplit` for more information about split fractions.
        """

        win0 = self.GetTopLeft()
        win1 = self.GetTopRight()
        win2 = self.GetBottomLeft()
        ##4Way## win3 = self.GetBottomRight()

        width, height = self.GetSize()
        barSize = self._GetSashSize()
        border = self._GetBorderSize()

        if self._expanded < 0:
            totw = width - barSize - 2 * border
            toth = height - barSize - 2 * border
            self._splitx = (self._fhor * totw) / 10000
            self._splity = (self._fver * toth) / 10000
            rightw = totw - self._splitx
            bottomh = toth - self._splity

            minimumSizeX = self._hSplitMinSizeX                # MinSizeMOD
            minimumSizeY = self._vSplitMinSizeY                # MinSizeMOD

            ##DEBUG print('totw = %s' % totw)
            ##DEBUG print('toth = %s' % toth)
            ##DEBUG print('width = %s' % width)
            ##DEBUG print('height = %s' % height)
            ##DEBUG print('rightw = %s' % rightw)
            ##DEBUG print('bottomh = %s' % bottomh)
            ##DEBUG print('minimumSizeX = %s' % minimumSizeX)
            ##DEBUG print('minimumSizeY = %s' % minimumSizeY)
            ##DEBUG print('self._splitx = %s' % self._splitx)
            ##DEBUG print('self._splity = %s' % self._splity)
            ##DEBUG print('self._fhor = %s' % self._fhor)
            ##DEBUG print('self._fver = %s' % self._fver)
            ##DEBUG print('self._offx = %s' % self._offx)
            ##DEBUG print('self._offy = %s' % self._offy)
            ##DEBUG print('-' * 30)

            if minimumSizeX or minimumSizeY:

                if self._splitx < minimumSizeX: # This section deals with dragging to the left
                    if self._splitx < minimumSizeX/2: # print('less than half')
                        oldsplitx = self._splitx
                        self._splitx = minimumSizeX
                        rightw = rightw - self._splitx + oldsplitx
                    elif self._splitx > minimumSizeX/2: # print('more than half')
                        oldsplitx = self._splitx
                        self._splitx = minimumSizeX
                        rightw = rightw - self._splitx + oldsplitx
                    else: # print('== half minimumSizeX')
                        self._splitx = minimumSizeX
                        rightw = rightw - minimumSizeX/2

                if self._splity < minimumSizeY: # This section deals with dragging to the top
                    if self._splity < minimumSizeY/2: # print('less than half')
                        oldsplity = self._splity
                        self._splity = minimumSizeY
                        bottomh = bottomh - self._splity + oldsplity
                    elif self._splity > minimumSizeY/2: # print('more than half')
                        oldsplity = self._splity
                        self._splity = minimumSizeY
                        bottomh = bottomh - self._splity + oldsplity
                    else: # print('== half minimumSizeY')
                        self._splity = minimumSizeY
                        bottomh = bottomh - minimumSizeY/2

                rightMinZone = totw - minimumSizeX
                if self._splitx > rightMinZone: # This section deals with dragging to the right
                    self._splitx = rightMinZone
                    rightw = totw - rightMinZone

                bottomMinZone = toth - minimumSizeY
                if self._splity > bottomMinZone: # This section deals with dragging to the bottom
                    self._splity = bottomMinZone
                    bottomh = toth - bottomMinZone

            splitx = self._splitx
            splity = self._splity

            # Order of windows are in clockwise fashion.
            if self._loneSide == wx.LEFT:
                # 3Way 1Left/2Right
                if win0:
                    win0.SetSize(0, 0, splitx, toth + barSize)
                    win0.Show()
                if win1:
                    win1.SetSize(splitx + barSize, 0, rightw, splity)
                    win1.Show()
                if win2:
                    win2.SetSize(splitx + barSize, splity + barSize, rightw, bottomh)
                    win2.Show()
            elif self._loneSide == wx.TOP:
                # 3Way 1Top/2Bottom
                if win0:
                    win0.SetSize(0, 0, rightw + splitx + barSize, splity)
                    win0.Show()
                if win1:
                    win1.SetSize(splitx + barSize, splity + barSize, rightw, bottomh)
                    win1.Show()
                if win2:
                    win2.SetSize(0, splity + barSize, splitx, bottomh)
                    win2.Show()
            elif self._loneSide == wx.RIGHT:
                # 3Way 1Right/2Left
                if win0:
                    win0.SetSize(splitx + barSize, 0, rightw, toth + barSize)
                    win0.Show()
                if win1:
                    win1.SetSize(0, splity + barSize, splitx, bottomh)
                    win1.Show()
                if win2:
                    win2.SetSize(0, 0, splitx, splity)
                    win2.Show()
            elif self._loneSide == wx.BOTTOM:
                # 3Way 2Top/1Bottom
                if win0:
                    win0.SetSize(0, splity + barSize, rightw + splitx + barSize, bottomh)
                    win0.Show()
                if win1:
                    win1.SetSize(0, 0, splitx, splity)
                    win1.Show()
                if win2:
                    win2.SetSize(splitx + barSize, 0, rightw, splity)
                    win2.Show()

            # Working fallback code without minsize calculations
            # if self._loneSide == wx.LEFT:
            #     # 3Way 1Left/2Right
            #     if win0:
            #         win0.SetSize(0, 0, splitx, toth + barSize)
            #         win0.Show()
            #     if win1:
            #         win1.SetSize(splitx + barSize, 0, rightw, splity)
            #         win1.Show()
            #     if win2:
            #         win2.SetSize(splitx + barSize, splity + barSize, rightw, bottomh)
            #         win2.Show()
            #
            # elif self._loneSide == wx.TOP:
            #     # 3Way 1Top/2Bottom
            #     if win0:
            #         win0.SetSize(0, 0, rightw + splitx + barSize, splity)
            #         win0.Show()
            #     if win1:
            #         win1.SetSize(splitx + barSize, splity + barSize, rightw, bottomh)
            #         win1.Show()
            #     if win2:
            #         win2.SetSize(0, splity + barSize, splitx, bottomh)
            #         win2.Show()
            #
            # elif self._loneSide == wx.RIGHT:
            #     # 3Way 1Right/2Left
            #     if win0:
            #         win0.SetSize(splitx + barSize, 0, rightw, toth + barSize)
            #         win0.Show()
            #     if win1:
            #         win1.SetSize(0, splity + barSize, splitx, bottomh)
            #         win1.Show()
            #     if win2:
            #         win2.SetSize(0, 0, splitx, splity)
            #         win2.Show()
            #
            # elif self._loneSide == wx.BOTTOM:
            #     # 3Way 2Top/1Bottom
            #     if win0:
            #         win0.SetSize(0, splity + barSize, rightw + splitx + barSize, bottomh)
            #         win0.Show()
            #     if win1:
            #         win1.SetSize(0, 0, splitx, splity)
            #         win1.Show()
            #     if win2:
            #         win2.SetSize(splitx + barSize, 0, rightw, splity)
            #         win2.Show()

            else:
                raise Exception('loneSide direction unknown!')

        else:

            if self._expanded < len(self._windows):
                for ii, win in enumerate(self._windows):
                    if ii == self._expanded:
                        win.SetSize(0, 0, width-2*border, height-2*border)
                        win.Show()
                    else:
                        win.Hide()


    # Determine split mode
    def GetMode(self, pt):
        """
        Determines the split mode for :class:`ThreeWaySplitter`.

        :param `pt`: the point at which the mouse has been clicked, an instance of
         :class:`Point`.

        :return: One of the following 3 split modes:

         ================= ==============================
         Split Mode        Description
         ================= ==============================
         ``wx.HORIZONTAL`` the user has clicked on the horizontal sash
         ``wx.VERTICAL``   The user has clicked on the vertical sash
         ``wx.BOTH``       The user has clicked at the intersection between the 2 sashes
         ================= ==============================

        """

        barSize = self._GetSashSize()
        flag = wx.BOTH

        if pt.x < self._splitx - _TOLERANCE:
            flag &= ~wx.VERTICAL

        if pt.y < self._splity - _TOLERANCE:
            flag &= ~wx.HORIZONTAL

        if pt.x >= self._splitx + barSize + _TOLERANCE:
            flag &= ~wx.VERTICAL

        if pt.y >= self._splity + barSize + _TOLERANCE:
            flag &= ~wx.HORIZONTAL

        return flag


    # Move the split intelligently
    def MoveSplit(self, x, y):
        """
        Moves the split accordingly to user action.

        :param `x`: the new splitter `x` coordinate;
        :param `y`: the new splitter `y` coordinate.
        """

        width, height = self.GetSize()
        barSize = self._GetSashSize()

        if x < 0: x = 0
        if y < 0: y = 0
        if x > width - barSize: x = width - barSize
        if y > height - barSize: y = height - barSize

        self._splitx = x
        self._splity = y


    # Adjust layout
    def AdjustLayout(self):
        """
        Adjust layout of :class:`ThreeWaySplitter`. Mainly used to recalculate the
        correct values for split fractions.
        """

        width, height = self.GetSize()
        barSize = self._GetSashSize()
        border = self._GetBorderSize()

        self._fhor = (width > barSize and \
                      [(10000*self._splitx+(width-barSize-1))/(width-barSize)] \
                      or [0])[0]

        self._fver = (height > barSize and \
                      [(10000*self._splity+(height-barSize-1))/(height-barSize)] \
                      or [0])[0]

        self._SizeWindows()


    # Button being pressed
    def OnLeftDown(self, event):
        """
        Handles the ``wx.EVT_LEFT_DOWN`` event for :class:`ThreeWaySplitter`.

        :param `event`: a :class:`MouseEvent` event to be processed.
        """

        if not self.IsEnabled():
            return

        pt = event.GetPosition()
        self.CaptureMouse()
        self._hasCapture = True
        self._mode = self.GetMode(pt)
        self._hasCaptureMode = self._mode

        if self._mode:
            self._offx = pt.x - self._splitx
            self._offy = pt.y - self._splity
            if not self.GetAGWWindowStyleFlag() & wx.SP_LIVE_UPDATE:
                self.DrawSplitter(wx.ClientDC(self))
                self.DrawTrackSplitter(self._splitx, self._splity)

            self._flags |= FLAG_PRESSED


    # Button being released
    def OnLeftUp(self, event):
        """
        Handles the ``wx.EVT_LEFT_UP`` event for :class:`ThreeWaySplitter`.

        :param `event`: a :class:`MouseEvent` event to be processed.
        """

        if not self.IsEnabled():
            return

        if self.HasCapture():
            self.ReleaseMouse()
            self._hasCapture = False
            self.SetCursor(wx.STANDARD_CURSOR)

        flgs = self._flags

        self._flags &= ~FLAG_CHANGED
        self._flags &= ~FLAG_PRESSED

        if flgs & FLAG_PRESSED:

            if not self.GetAGWWindowStyleFlag() & wx.SP_LIVE_UPDATE:
                self.DrawTrackSplitter(self._splitx, self._splity)
                self.DrawSplitter(wx.ClientDC(self))
                self.AdjustLayout()

            if flgs & FLAG_CHANGED:
                event = ThreeWaySplitterEvent(wx.wxEVT_COMMAND_SPLITTER_SASH_POS_CHANGED, self)
                event.SetSashIdx(self._mode)
                event.SetSashPosition(wx.Point(self._splitx, self._splity))
                self.GetEventHandler().ProcessEvent(event)

        self._mode = NOWHERE
        self._hasCaptureMode = NOWHERE


    def OnLeaveWindow(self, event):
        """
        Handles the ``wx.EVT_LEAVE_WINDOW`` event for :class:`ThreeWaySplitter`.

        :param `event`: a :class:`MouseEvent` event to be processed.
        """
        if not self._hasCapture:
            self.SetCursor(wx.STANDARD_CURSOR)
        self._RedrawIfHotSensitive(False)


    def OnEnterWindow(self, event):
        """
        Handles the ``wx.EVT_ENTER_WINDOW`` event for :class:`ThreeWaySplitter`.

        :param `event`: a :class:`MouseEvent` event to be processed.
        """

        self._RedrawIfHotSensitive(True)

        # Change cursor based on if mouse had capture when leaving.
        # Ex: Splitter is still being dragged; Left mouse btn is still down.
        hasCapture = wx.GetMouseState().LeftIsDown()

        if self._mode == wx.BOTH and hasCapture:
            self.SetCursor(self._sashCursorSIZING)

        elif self._mode == wx.VERTICAL and hasCapture:
            self.SetCursor(self._sashCursorWE)

        elif self._mode == wx.HORIZONTAL and hasCapture:
            self.SetCursor(self._sashCursorNS)


    def _RedrawIfHotSensitive(self, isHot):
        """
        Used internally. Redraw the splitter if we are using a hot-sensitive splitter.

        :param `isHot`: ``True`` if the splitter is in a hot state, ``False`` otherwise.
        """

        if not wx.VERSION >= _RENDER_VER:
            return

        if wx.RendererNative.Get().GetSplitterParams(self).isHotSensitive:
            self._isHot = isHot
            dc = wx.ClientDC(self)
            self.DrawSplitter(dc)


    def OnMotion(self, event):
        """
        Handles the ``wx.EVT_MOTION`` event for :class:`ThreeWaySplitter`.

        :param `event`: a :class:`MouseEvent` event to be processed.
        """

        if self.HasFlag(wx.SP_NOSASH):
            return

        pt = event.GetPosition()

        # Moving split
        if self._flags & FLAG_PRESSED:

            oldsplitx = self._splitx
            oldsplity = self._splity

            if self._mode == wx.BOTH:
                self.MoveSplit(pt.x - self._offx, pt.y - self._offy)

            elif self._mode == wx.VERTICAL:
                self.MoveSplit(pt.x - self._offx, self._splity)

            elif self._mode == wx.HORIZONTAL:
                self.MoveSplit(self._splitx, pt.y - self._offy)

            # Send a changing event
            if not self.DoSendChangingEvent(wx.Point(self._splitx, self._splity)):
                self._splitx = oldsplitx
                self._splity = oldsplity
                return

            if oldsplitx != self._splitx or oldsplity != self._splity:
                if not self.GetAGWWindowStyleFlag() & wx.SP_LIVE_UPDATE:
                    self.DrawTrackSplitter(oldsplitx, oldsplity)
                    self.DrawTrackSplitter(self._splitx, self._splity)
                else:
                    self.AdjustLayout()

                self._flags |= FLAG_CHANGED

        # Change cursor based on position
        ff = self.GetMode(pt)
        hasCapture = self._hasCapture
        # self._hasCaptureMode = ff

        if self._hasCaptureMode == wx.BOTH and not hasCapture or ff == wx.BOTH and not hasCapture:
            self.SetCursor(self._sashCursorSIZING)

        elif ff == wx.VERTICAL and not hasCapture:
            self.SetCursor(self._sashCursorWE)

        elif ff == wx.HORIZONTAL and not hasCapture:
            self.SetCursor(self._sashCursorNS)

        elif not hasCapture:
            self.SetCursor(wx.STANDARD_CURSOR)

        event.Skip()

    def OnPaint(self, event):
        """
        Handles the ``wx.EVT_PAINT`` event for :class:`ThreeWaySplitter`.

        :param `event`: a :class:`PaintEvent` event to be processed.
        """

        dc = wx.PaintDC(self)
        self.DrawSplitter(dc)


    def OnSize(self, event):
        """
        Handles the ``wx.EVT_SIZE`` event for :class:`ThreeWaySplitter`.

        :param `event`: a :class:`SizeEvent` event to be processed.
        """

        parent = wx.GetTopLevelParent(self)
        if parent.IsIconized():
            event.Skip()
            return

        self._SizeWindows()


    def DoSendChangingEvent(self, pt):
        """
        Sends a ``EVT_SPLITTER_SASH_POS_CHANGING`` event.

        :param `pt`: the point at which the splitter is being positioned.
        """

        # send the event
        event = ThreeWaySplitterEvent(wx.wxEVT_COMMAND_SPLITTER_SASH_POS_CHANGING, self)
        event.SetSashIdx(self._mode)
        event.SetSashPosition(pt)

        if self.GetEventHandler().ProcessEvent(event) and not event.IsAllowed():
            # the event handler vetoed the change or missing event.Skip()
            return False
        else:
            # or it might have changed the value
            return True


    def _GetSashSize(self):
        """ Used internally. """

        if self.HasFlag(wx.SP_NOSASH):
            return 0

        if wx.VERSION >= _RENDER_VER:
            return wx.RendererNative.Get().GetSplitterParams(self).widthSash
        else:
            return 5


    def _GetBorderSize(self):
        """ Used internally. """

        if wx.VERSION >= _RENDER_VER:
            return wx.RendererNative.Get().GetSplitterParams(self).border
        else:
            return 0


    # Draw the horizontal split
    def DrawSplitter(self, dc):
        """
        Actually draws the sashes.

        :param `dc`: an instance of :class:`DC`.
        """

        backColour = self.GetBackgroundColour()
        dc.SetBrush(wx.Brush(backColour, wx.BRUSHSTYLE_SOLID))
        dc.SetPen(wx.Pen(backColour))
        dc.Clear()

        if wx.VERSION >= _RENDER_VER:
            if self.HasFlag(wx.SP_3DBORDER):
                wx.RendererNative.Get().DrawSplitterBorder(
                    self, dc, self.GetClientRect())
        else:
            barSize = self._GetSashSize()

        # if we are not supposed to use a sash then we're done.
        if self.HasFlag(wx.SP_NOSASH):
            return

        flag = 0
        if self._isHot:
            flag = wx.CONTROL_CURRENT

        width, height = self.GetSize()

        if self._mode & wx.VERTICAL:
            if wx.VERSION >= _RENDER_VER:
                wx.RendererNative.Get().DrawSplitterSash(self, dc,
                                                         self.GetClientSize(),
                                                         self._splitx, wx.VERTICAL, flag)
            else:
                dc.DrawRectangle(self._splitx, 0, barSize, height)

        if self._mode & wx.HORIZONTAL:
            if wx.VERSION >= _RENDER_VER:
                wx.RendererNative.Get().DrawSplitterSash(self, dc,
                                                         self.GetClientSize(),
                                                         self._splity, wx.VERTICAL, flag)
            else:
                dc.DrawRectangle(0, self._splity, width, barSize)


    def DrawTrackSplitter(self, x, y):
        """
        Draws a fake sash in case we don't have ``wx.SP_LIVE_UPDATE`` style.

        :param `x`: the `x` position of the sash;
        :param `y`: the `y` position of the sash.

        :note: This method relies on :class:`ScreenDC` which is currently unavailable on wxMac.
        """

        # Draw a line to represent the dragging sash, for when not
        # doing live updates
        w, h = self.GetClientSize()
        dc = wx.ScreenDC()

        dc.SetLogicalFunction(wx.INVERT)
        dc.SetPen(self._sashTrackerPen)
        dc.SetBrush(wx.TRANSPARENT_BRUSH)

        if self._mode == wx.VERTICAL:
            x1 = x
            y1 = 2
            x2 = x
            y2 = h-2
            if x1 > w:
                x1 = w
                x2 = w
            elif x1 < 0:
                x1 = 0
                x2 = 0

            x1, y1 = self.ClientToScreen((x1, y1))
            x2, y2 = self.ClientToScreen((x2, y2))

            dc.DrawLine(x1, y1, x2, y2)
            dc.SetLogicalFunction(wx.COPY)

        elif self._mode == wx.HORIZONTAL:

            x1 = 2
            y1 = y
            x2 = w-2
            y2 = y
            if y1 > h:
                y1 = h
                y2 = h
            elif y1 < 0:
                y1 = 0
                y2 = 0

            x1, y1 = self.ClientToScreen((x1, y1))
            x2, y2 = self.ClientToScreen((x2, y2))

            dc.DrawLine(x1, y1, x2, y2)
            dc.SetLogicalFunction(wx.COPY)

        elif self._mode == wx.BOTH:

            x1 = 2
            x2 = w-2
            y1 = y
            y2 = y

            x1, y1 = self.ClientToScreen((x1, y1))
            x2, y2 = self.ClientToScreen((x2, y2))

            dc.DrawLine(x1, y1, x2, y2)

            x1 = x
            x2 = x
            y1 = 2
            y2 = h-2

            x1, y1 = self.ClientToScreen((x1, y1))
            x2, y2 = self.ClientToScreen((x2, y2))

            dc.DrawLine(x1, y1, x2, y2)
            dc.SetLogicalFunction(wx.COPY)


    # Change horizontal split [fraction*10000]
    def SetHSplit(self, s):
        """
        Change horizontal split fraction.

        :param `s`: the split fraction, which is an integer value between 0 and
         10000 (inclusive), indicating how much space to allocate to the leftmost
         panes. For example, to split the panes at 35 percent, use::

            threeSplitter.SetHSplit(3500)

        """
        if s < 0: s = 0
        if s > 10000: s = 10000
        if s != self._fhor:
            self._fhor = s
            self._SizeWindows()


    # Change vertical split [fraction*10000]
    def SetVSplit(self, s):
        """
        Change vertical split fraction.

        :param `s`: the split fraction, which is an integer value between 0 and
         10000 (inclusive), indicating how much space to allocate to the topmost
         panes. For example, to split the panes at 35 percent, use::

            threeSplitter.SetVSplit(3500)

        """
        if s < 0: s = 0
        if s > 10000: s = 10000
        if s != self._fver:
            self._fver = s
            self._SizeWindows()


    def GetExpandedWindow(self):
        """
        Get the window instance that is expanded.

        :returns: The expanded window instance.
        :rtype: :class:`Window`
        """
        return self._windows[self._expanded]


    def GetExpanded(self):
        """
        Get the index of the expanded window.

        :returns: The expanded window index. -1 means no window is currently expanded.
        :rtype: int
        """
        return self._expanded


    def IsWindowExpanded(self, index):
        """
        Get whether the window index is expanded.

        :param `index`: An index integer to check against. 0 - 2
        :type `index`: int
        :returns: ``True`` if the index is expanded, ``False`` otherwise.
        :rtype: bool
        """
        return index == self._expanded


    def GetWindowIndex(self, win):
        """
        Get the index of the sent window instance.

        :param `win`: an instance of :class:`Window`
        :type `win`: :class:`Window`
        :returns: The index of the window(zero-based), -1 otherwise if not a
         child of :class:`ThreeWaySplitter`.
        :rtype: int
        """
        if win in self._windows:
            return self._windows.index(win)

        return -1


    # Expand one or all of the three panes
    def SetExpanded(self, expanded):
        """
        This method is used to expand one of the three windows to fill the
        whole client size (when `expanded` >= 0) or to return to the three-window
        view (when `expanded` < 0).

        :param `expanded`: an integer >= 0 to expand a window to fill the whole
         client size, or an integer < 0 to return to the three-window view.
        """

        if expanded >= 3:
            raise Exception("ERROR: SetExpanded: index out of range: %d"%expanded)

        if self._expanded != expanded:
            self._expanded = expanded
            self._SizeWindows()


if __name__ == '__main__':
    # Test app.

    class SampleGradientPanel(wx.Panel):
        def __init__(self, parent, gradColours):
            wx.Panel.__init__(self, parent)
            self.gradColours = gradColours
            self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)
            self.Bind(wx.EVT_PAINT, self.OnPaint)
            self.Bind(wx.EVT_SIZE, self.OnSize)

        def OnEraseBackground(self, event):
            pass

        def OnSize(self, event):
            self.Refresh()

        def OnPaint(self, event):
            dc = wx.PaintDC(self) # More buffering will slow down the AnimationMoves.
            dc.GradientFillLinear(self.GetClientRect(),
                                  self.gradColours[0], self.gradColours[1])


    class ThreeWaySplitterFrame(wx.Frame):
        def __init__(self, parent, id=wx.ID_ANY, title=wx.EmptyString,
                     pos=wx.DefaultPosition, size=wx.DefaultSize,
                     style=wx.DEFAULT_FRAME_STYLE, name='frame'):
            wx.Frame.__init__(self, parent, id, title, pos, size, style, name)

            splitter = ThreeWaySplitter(self, agwStyle=wx.SP_LIVE_UPDATE,
                                        loneSide=wx.TOP, minSplitterSize=(50, 50))

            for ii, color in enumerate((wx.RED, '#FFFF00', wx.Colour(0, 0, 255))):
                panel = SampleGradientPanel(splitter, (color, wx.WHITE))
                splitter.AppendWindow(panel)

            self.Bind(wx.EVT_CLOSE, self.OnDestroy)
            
            self.CreateStatusBar().SetStatusText('wxPython %s' % wx.version())

        def OnDestroy(self, event):
            self.Destroy()


    class ThreeWaySplitterApp(wx.App):
        def OnInit(self):
            gMainWin = ThreeWaySplitterFrame(None, size=(350, 350))
            gMainWin.SetTitle('ThreeWaySplitter Test')
            self.SetTopWindow(gMainWin)
            gMainWin.Show()
            return True


    gApp = ThreeWaySplitterApp(redirect=False,
            filename=None,
            useBestVisual=False,
            clearSigInt=True)

    gApp.MainLoop()
