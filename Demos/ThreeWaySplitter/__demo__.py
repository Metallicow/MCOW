#!/usr/bin/env python

"""
This module contains the meta data needed for integrating the samples
in the mcow subdir into the wxPython demo framework. Once imported,
this module returns the following information:

* GetDemoBitmap: returns the bitmap used in the wxPython tree control
  to characterize the User's package;
* GetRecentAdditions: returns a subset (or the whole set) of demos in
  the User's package which will appear under the Recent Additions tree
  item in the wxPython demo;
* GetDemos: returns all the demos in the User's package;
* GetOverview: returns a wx.html-ready representation of the User's docs.

These meta data are merged into the wxPython demo tree at startup.

Last updated: Metallicow @ 08 Aug 2013, 21.00 GMT.
Version 0.0.1

"""

__version__ = "0.0.1"
__author__ = "Metallicow"


# Start the imports...



import wx
from wx.lib.embeddedimage import PyEmbeddedImage

import wx.lib.mcow.threewaysplitter


def GetDemoBitmap():
    """ Returns the bitmap to be used in the demo tree for the User's package. """

    # Get the image as PyEmbeddedImage
    image = PyEmbeddedImage(
    "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAACXBIWXMAAA7DAAAOwwHHb6hk"
    "AAAABGdBTUEAALGOfPtRkwAAACBjSFJNAAB6JQAAgIMAAPn/AACA6QAAdTAAAOpgAAA6mAAA"
    "F2+SX8VGAAAA0ElEQVR42mL8//8/AyUAIICYGCgEAAFEsQEAAcQCYzAyMhLtF6C3GWFsgABi"
    "QZYQ/S/JIM8gyyDIIMAgzCAChuoMamA6kjGC4fT/0wymjKYohgEEENFe2PV/F8R2iHPhrgUI"
    "IJBzGKAx8R/ogv9QNXjxf7AvIPoAAogF3SaT/2ZYvSDMIAQUF4R4ASkMAAIIxQWEMDAMIC6A"
    "6gFhgAAiOhBBLsAGAAKIvDBAcgFAAJEXBkgAIIAYYXmB3IQEEECMlGYmgACiOC8ABBDFBgAE"
    "GABobneg5xygCgAAAABJRU5ErkJggg==")

    # Return the bitmap to use in the wxPython demo tree control.
    return image


def GetRecentAdditions():
    """
    Returns a subset (or the full set) of the User's demo names which will go
    into the Recent Additions tree item in the wxPython demo.
    """

    # For the moment, we add all the widgets in User's Package as
    # Recent Additions
    recentAdditions = ['ExceptionHookDialogDemo', 'STC_SmartHighlighting',
        'WindowBorderStyles', 'GradientButtonMaker', 'ExtractImages',
        'ImageCount', 'wxPytrix', 'ClassicVsPhoenix']

    # Return the Recent Additions for MCow
    return recentAdditions


def GetDemos():
    """
    Returns all the demo names in the AGW package, together with the tree item
    name which will go in the wxPython demo tree control.
    """

    # The tree item text for MCow
    UsersTreeItem = "ThreeWaySplitter"

    # The MCow demos
    UsersDemos = ['ThreeWaySplitter',
                  'ThreeWaySplitter_windows',
                  ]

    return UsersTreeItem, UsersDemos


def GetOverview():
    """
    Creates the HTML code to display the User's Demos
    """
    docs = wx.lib.mcow.threewaysplitter.__doc__
    str = (docs.replace(':class:', '').
                replace(':mod:', ''))

    #--DocUtils Imports.
    try:
        from docutils.core import publish_string
        overview = publish_string(docs, writer_name='html')
    except ImportError:
        overview = docs


    str = '''\
    Most all demos are Classic/Phoenix Compatible Code.
    '''

    return overview

