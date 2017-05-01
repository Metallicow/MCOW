#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This is the Meticulously Crafted Optimal Widgets package (MCOW).

adj. me tic u lous
    1. Extremely careful and precise.
    2. Extremely or excessively concerned with details.

tr.v. craft ed
    1. To make by hand.
    2. Usage Problem To make or construct (something) in a manner suggesting great care or ingenuity.

adj. op ti mal
    1. Most favorable or desirable; optimum.

n. widg its
    1. Graphical user interface(GUI) elements.


"Ohhh! Shiny!"
It provides many custom-drawn wxPython controls: some of them can be used as a replacement
of the platform native controls, others are simply an addition to the
already rich wxPython widgets set.


Description:

MCOW contains many different modules and mixins, listed below.

- ShapedBitmapButton: this class fills the lack of "custom shaped" controls
  in wxPython. It can be used to build round or custom-shaped buttons from images with
  alpha(PNG). It is a special Ultra-Useful-All-In-One control, capable of producing
  professional looking graphical custom buttons/windows/etc very easily.;
- SmartHighlighting: a mixin for the StyledTextCtrl that provides quick
  highlighting effects for text.;
- ThreeWaySplitter: this is a layout manager which manages three children similar to
  Andrea Gavana's AGW FourWaySplitter. ThreeWaySplitters(generally) are quite
  more often needed/used than FourWaySplitters.
  Modifications/Additions by me on top of Andrea's FourWaySplitter Code.;
- Picture: is a scalable picture window like ones often used in image viewer
  applications. It provides Overscaling and Downscaling toggleable options.
  Background Color is customizable and can be a tiled texture if desired.;
- Animation: Basic animation functions for windows.


Bugs and Limitations: many, patches and fixes welcome :-D

See the demos for an example of what MCOW can do, and on how to use it.


License: Same as the version of wxPython you are using it with.

GitHub for latest code:
https://github.com/Metallicow/MCOW

Mailing List:
wxpython-users@lists.wxwidgets.org


Please let me know if you are using MCOW!

You can contact me at:

metaliobovinus at gmail dot com

"""

__author__ = "Edward Greig <metaliobovinus@gmail.com>"
