#!/usr/bin/env python

#----------------------------------------------------------------------------
# Name:        wx.lib.mcow.mixins.styledtextctrl
# Purpose:     Helpful mix-in classes for wx.stc.StyledTextCtrl
#
# Author:      Edward Greig
#
# Created:     Phoenix-STC-2013
# Copyright:   (c) Edward Greig 2013
# Licence:     wxWindows license
#----------------------------------------------------------------------------

import re

import wx
import wx.stc as stc

#----------------------------------------------------------------------------

# Mode Flags
CASESENSITIVE = 0  # Do case-sensitive matches.
IGNORECASE = re.IGNORECASE  # Do case-insensitive matches.


class SmartHighlighterMixin:
    """SourceCoder Library: SmartHighlighterMixin
    Mixin class that handles automatic smart highlighting of text in a
    StyledTextCtrl.

    """
    def __init__(self, onTheFlyColor='#00FF00', onTheFlyIndic=stc.STC_INDIC_ROUNDBOX,
                 onTheFlyMode=IGNORECASE, permanentMode=CASESENSITIVE,
                 permanentColors=['#0000FF',
                                  '#FF0000',
                                  '#00FFFF',
                                  '#FFFF00',
                                  '#C0C0C0',
                                  '#000000',
                                  '#FF8000',
                                  '#FF00FF',
                                  '#FF69B4']):
        """Initialize the smart highlighter mixin
        :param `onTheFlyColor`: Set a custom highlight color (default wx.GREEN)
        :param `onTheFlyMode`: IGNORECASE (default) or CASESENSITIVE
        :param `permanentMode`: CASESENSITIVE (default) or IGNORECASE

        """
        # Attributes
        self._shOnTheFlyColor = onTheFlyColor
        self._shPermanentColors = permanentColors
        self._shOnTheFlyMode = onTheFlyMode
        self._shPermanentMode = permanentMode
        self._shOnTheFlyIndic = onTheFlyIndic
        self._forHighlighterPerformance = (0, 0)
        self.highlightTextDict = {}

        self.HIGHLIGHTERSTYLE00 = 20  # On-The-Fly Highlighter
        self.HIGHLIGHTERSTYLE01 = 21
        self.HIGHLIGHTERSTYLE02 = 22
        self.HIGHLIGHTERSTYLE03 = 23
        self.HIGHLIGHTERSTYLE04 = 24
        self.HIGHLIGHTERSTYLE05 = 25
        self.HIGHLIGHTERSTYLE06 = 26
        self.HIGHLIGHTERSTYLE07 = 27
        self.HIGHLIGHTERSTYLE08 = 28
        self.HIGHLIGHTERSTYLE09 = 29

        self.IndicatorSetStyle(self.HIGHLIGHTERSTYLE00, self._shOnTheFlyIndic)
        self.IndicatorSetForeground(self.HIGHLIGHTERSTYLE00, self._shOnTheFlyColor)
        self.IndicatorSetAlpha(self.HIGHLIGHTERSTYLE00, 64)

        ii = 0
        self_IndicatorSetStyle = self.IndicatorSetStyle
        self_IndicatorSetForeground = self.IndicatorSetForeground
        self_IndicatorSetAlpha = self.IndicatorSetAlpha
        for i in range(self.HIGHLIGHTERSTYLE01,
                       self.HIGHLIGHTERSTYLE09 + 1):
            self_IndicatorSetStyle(i, self._shOnTheFlyIndic)
            self_IndicatorSetForeground(i, self._shPermanentColors[ii])
            self_IndicatorSetAlpha(i, 64)
            ii += 1

        self.SetIndicatorCurrent(self.HIGHLIGHTERSTYLE00)

        # Event Handlers
        self.Bind(stc.EVT_STC_UPDATEUI, self._OnSTCUpdateUI)
        self.Bind(stc.EVT_STC_DOUBLECLICK, self._OnSTCDoubleClick)

    def _OnSTCUpdateUI(self, event):
        """
        Handles the ``wx.stc.EVT_STC_UPDATEUI`` event for :class:`StyledTextCtrl`.

        :param `event`: a :class:`UpdateUIEvent` event to be processed.
        """
        ## if not (self.GetSelectionStart(), self.GetSelectionEnd()) == self._forHighlighterPerformance:
        if not self.GetSelection() == self._forHighlighterPerformance:
            # Scrolling performance achieved here.
            self.HighlightSelectionOnTheFly()

        event.Skip()

    def _OnSTCDoubleClick(self, event):
        """
        Handles the ``wx.stc.EVT_STC_DOUBLECLICK`` event for :class:`StyledTextCtrl`.

        :param `event`: a :class:`MouseEvent` event to be processed.
        """
        self.HighlightSelectionOnTheFly()

        event.Skip()

    def OnHighlightText(self, event):
        """
        Check event id to determine what highlighter style to use,
        then permanently highlight text.
        """
        evtId = event.GetId()
        print('evtId', evtId)
        strId = str(evtId)
        if   strId.endswith('01'): highlighterStyle=self.HIGHLIGHTERSTYLE01
        elif strId.endswith('02'): highlighterStyle=self.HIGHLIGHTERSTYLE02
        elif strId.endswith('03'): highlighterStyle=self.HIGHLIGHTERSTYLE03
        elif strId.endswith('04'): highlighterStyle=self.HIGHLIGHTERSTYLE04
        elif strId.endswith('05'): highlighterStyle=self.HIGHLIGHTERSTYLE05
        elif strId.endswith('06'): highlighterStyle=self.HIGHLIGHTERSTYLE06
        elif strId.endswith('07'): highlighterStyle=self.HIGHLIGHTERSTYLE07
        elif strId.endswith('08'): highlighterStyle=self.HIGHLIGHTERSTYLE08
        elif strId.endswith('09'): highlighterStyle=self.HIGHLIGHTERSTYLE09
        self.HighlightTextPermanently(highlighterStyle=highlighterStyle)

    def OnUnhighlightStyle(self, event):
        evtId = event.GetId()
        print('evtId', evtId)
        strId = str(evtId)
        if   strId.endswith('01'): highlighterStyle=self.HIGHLIGHTERSTYLE01
        elif strId.endswith('02'): highlighterStyle=self.HIGHLIGHTERSTYLE02
        elif strId.endswith('03'): highlighterStyle=self.HIGHLIGHTERSTYLE03
        elif strId.endswith('04'): highlighterStyle=self.HIGHLIGHTERSTYLE04
        elif strId.endswith('05'): highlighterStyle=self.HIGHLIGHTERSTYLE05
        elif strId.endswith('06'): highlighterStyle=self.HIGHLIGHTERSTYLE06
        elif strId.endswith('07'): highlighterStyle=self.HIGHLIGHTERSTYLE07
        elif strId.endswith('08'): highlighterStyle=self.HIGHLIGHTERSTYLE08
        elif strId.endswith('09'): highlighterStyle=self.HIGHLIGHTERSTYLE09
        self.SetIndicatorCurrent(highlighterStyle)
        self.IndicatorClearRange(0, self.GetLength())
        self.SetIndicatorCurrent(self.HIGHLIGHTERSTYLE00) # Set back to On-The-Fly Highlighter after done.
        delthese = []
        # for text, style in six.iteritems(self.highlightTextDict):
        for text, style in list(self.highlightTextDict.items()):
            if style == highlighterStyle:
                delthese.append(text)
        for text in delthese:
            del self.highlightTextDict[text]
        self.OnSelectNone()
        self.HighlightTextPermanently(highlighterStyle=highlighterStyle)

    def OnUnhighlightText(self, event):
        self.UnhighlightText()

    def OnUnhighlightAll(self, event):
        """
        Unhighlight all styles... The permanently highlighted stuff.
        """
        for style in range(self.HIGHLIGHTERSTYLE01, self.HIGHLIGHTERSTYLE09 + 1):
            self.SetIndicatorCurrent(style)
            self.IndicatorClearRange(0, self.GetLength())
        self.SetIndicatorCurrent(self.HIGHLIGHTERSTYLE00) # Set back to On-The-Fly Highlighter after done.
        self.highlightTextDict = {}

    def HighlightSelectionOnTheFly(self, text=None):
        """
        Highlight Current Selection Matchs On-The-Fly.

        timeit test Py2.7.5 x1000
        stc.STC_FIND_REGEXP Method
        FindText: [11.085237626693713, 11.154881154332408, 11.089765059677294]
        re Method
        Regex: [7.711642673014154, 7.711089617365346, 7.718059265515734]
        """
        # Indicator style should be default On-The-Fly Highlighter
        # at this point, but set again just in case.
        self.SetIndicatorCurrent(self.HIGHLIGHTERSTYLE00)

        self.IndicatorClearRange(0, self.GetLength())
        text = text or self.GetSelectedText()
        charList = [' ','.','!','?', ',',':',';','"',"'",'(',')','[',']','<','>','{','}','|','\\','/','*','&','@','#','+','$','%','^','`','~','=','+']
        for item in charList:
            if item in text:
                # print('foundChar in charList')
                return
        if not text or '\r' in text or '\n' in text:
            return
        if text in self.highlightTextDict:
            return
        selstart = self.GetSelectionStart()
        selend = self.GetSelectionEnd()

        length = len(text)
        count = 0

        for match in re.finditer(r'\b%s\b' %(text), self.GetText(), flags=self._shOnTheFlyMode): # \b matches word boundary.
            self.IndicatorFillRange(position=match.start(), fillLength=length)
            count += 1
        if count == 1: # Unhighlight current caret selection if only 1 found.
            if selstart > selend:
                selstart, selend = selend, selstart
            self.IndicatorClearRange(position=selstart, clearLength=length)

        self._forHighlighterPerformance = (selstart, selend)
        ## print('count: %s text: %s' %(count, text))


    def HighlightSelectionsWithPermantentMarker(self):
        """
        timeit.repeat Test Py2.7.5
        stc.STC_FIND_REGEXP method
        FindText: [1.7875809046949023, 1.7837719813146862, 1.7834051116761778]
        re method
        Regex: [1.4007414816111066, 1.4018309157660909, 1.3992097969329222]
        """
        for style in range(self.HIGHLIGHTERSTYLE01, self.HIGHLIGHTERSTYLE09 + 1):
            self.SetIndicatorCurrent(style)
            self.IndicatorClearRange(0, self.GetLength())
        ## for text, highlighterStyle in six.iteritems(self.highlightTextDict):
        for text, highlighterStyle in list(self.highlightTextDict.items()):
            if not text:
                return
            self.SetIndicatorCurrent(highlighterStyle)
            length = len(text)

            for match in re.finditer(text, self.GetText(), flags=self._shPermanentMode):
                self.IndicatorFillRange(position=match.start(), fillLength=length)

        self.SetIndicatorCurrent(self.HIGHLIGHTERSTYLE00)#Set back to On-The-Fly Highlighter after done.
        ## print('self.highlightTextDict = ', self.highlightTextDict)


    def HighlightTextPermanently(self, text=None, highlighterStyle=None, flags=None):
        text = text or self.GetSelectedText()
        if text:
            print('PermanentHighlight')
            # Add the text to the dictionary for permanent highlighting.
            self.highlightTextDict[text] = highlighterStyle
            self.HighlightSelectionsWithPermantentMarker()

    def UnhighlightText(self, text=None):
        text = text or self.GetSelectedText()
        if text in self.highlightTextDict:
            del self.highlightTextDict[text]
            self.HighlightSelectionsWithPermantentMarker()


#----------------------------------------------------------------------------

import wx.lib.agw.cubecolourdialog as CCD

DEFAULTCOLORDIALOG = 0
COLOURCUBEDIALOG = 1

class DoubleClickColorPickMixin:
    """SourceCoder Library: DoubleClickColorPickMixin
    Mixin class that handles changing of hexadecimal colors in text in a
    StyledTextCtrl by DoubleClicking on a hex string such as '#000000'.

    """
    def __init__(self, dialogMode=COLOURCUBEDIALOG):
        """Initialize the doubleclick colorpick mixin
        @keyword dialogMode: DEFAULTCOLORDIALOG (default) or COLOURCUBEDIALOG

        """
        # Attributes
        self._dialogMode = dialogMode

        self.Bind(stc.EVT_STC_DOUBLECLICK, self.OnDoubleClickColorPick)

    def OnDoubleClickColorPick(self, event):
        selText = self.GetSelectedText().lower()
        if not len(selText) in (3, 6):
            return
        for char in selText:
            if not char in ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f'):
                return
        if not self.GetCharAt(self.GetSelectionStart() - 1) == ord('#'):
            return
        selStart, selEnd = self.GetSelectionStart(), self.GetSelectionEnd()

        cd = wx.ColourData()
        hexColor = selText if len(selText) == 6 else '%s%s%s' % (selText[0] * 2,
                                                                 selText[1] * 2,
                                                                 selText[2] * 2)
        cd.SetColour(u'#%s' % hexColor)
        cc = ('#FFFFFF', '#EEEEEE', '#DDDDDD', '#CCCCCC',
              '#BBBBBB', '#AAAAAA', '#999999', '#888888',
              '#777777', '#666666', '#555555', '#444444',
              '#333333', '#222222', '#111111', '#000000')
        for i, col in enumerate(cc):
            cd.SetCustomColour(i, col)
        ColorHexString = self.ColorCubeDialog(self, colorData=cd)
        if ColorHexString:
            if len(selText) == 3 and (ColorHexString[1] == ColorHexString[2]) \
                                 and (ColorHexString[3] == ColorHexString[4]) \
                                 and (ColorHexString[5] == ColorHexString[6]):
                # Shorten back to #FFF three char hex.
                self.ReplaceSelection(u'%s%s%s' % (ColorHexString[1],
                                                   ColorHexString[3],
                                                   ColorHexString[5]))
            else:
                # Leave as #FFFFFF six char hex
                # Adjust for added alpha to hex. back to 6, not 8.
                self.ReplaceSelection(u'%s' % ColorHexString.lstrip('#')[:-2])


    def ColorCubeDialog(self, parent, colorData=None, uppercase=True, showAlpha=True):
        """"""
        ColorHexString = 0
        if showAlpha:
            dialog = CCD.CubeColourDialog(parent, colorData, agwStyle=CCD.CCD_SHOW_ALPHA)
        else:
            dialog = CCD.CubeColourDialog(parent, colorData, agwStyle=0)
        if dialog.ShowModal() == wx.ID_OK:

            # If the user selected OK, then the dialog's wx.ColourData will contain valid information. Fetch the data ...
            ## self.colourData = dialog.GetColourData()
            colorData = dialog.GetColourData()
            h, s, v, a = dialog.GetHSVAColour()

            # ... then do something with it. The actual colour data will be returned as a three-tuple (r, g, b) in this particular case.
            data = dialog.GetColourData()
            color = data.GetColour()
            ## print('color.Get() = ', color.Get())

            ColorHexString = '#%02x%02x%02x%02x' % color.Get()

            if uppercase:
                ColorHexString = ColorHexString.upper() # UpperCase the hexstring.
            else:
                ColorHexString = ColorHexString.lower() # LowerCase the hexstring.

            ## print('You selected: %s\n' %(data.GetColour().Get()))
            ## print(ColorHexString)
            dialog.Destroy()
        else:
            ## print('Canceled Color Cube')
            dialog.Destroy()
        return ColorHexString


#----------------------------------------------------------------------------


if __name__ == '__main__':
    # Test App.
    import sys

    class PlainSTC(stc.StyledTextCtrl, SmartHighlighterMixin, DoubleClickColorPickMixin):
        def __init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition,
                     size=wx.DefaultSize, style=0, name='styledtextctrl'):
            stc.StyledTextCtrl.__init__(self, parent, id, pos, size, style, name)

            DoubleClickColorPickMixin.__init__(self)

            SmartHighlighterMixin.__init__(self)

            self.SetText('DoubleClickColorPickMixin #FF8000\n\n' +
                         'SmartHighlighterMixin\n\n' +
                         ('StyledTextCtrl\n    Smart Highlighter Mixin\n'
                          '        PermanentColor1\n'
                          '        PermanentColor2\n'
                          '        PermanentColor3\n'
                          '        PermanentColor4\n'
                          '        PermanentColor5\n'
                          '        PermanentColor6\n'
                          '        PermanentColor7\n'
                          '        PermanentColor8\n'
                          '        PermanentColor9\n') * 500)

            self.HighlightTextPermanently('PermanentColor1', self.HIGHLIGHTERSTYLE01)
            self.HighlightTextPermanently('PermanentColor2', self.HIGHLIGHTERSTYLE02)
            self.HighlightTextPermanently('PermanentColor3', self.HIGHLIGHTERSTYLE03)
            self.HighlightTextPermanently('PermanentColor4', self.HIGHLIGHTERSTYLE04)
            self.HighlightTextPermanently('PermanentColor5', self.HIGHLIGHTERSTYLE05)
            self.HighlightTextPermanently('PermanentColor6', self.HIGHLIGHTERSTYLE06)
            self.HighlightTextPermanently('PermanentColor7', self.HIGHLIGHTERSTYLE07)
            self.HighlightTextPermanently('PermanentColor8', self.HIGHLIGHTERSTYLE08)
            self.HighlightTextPermanently('PermanentColor9', self.HIGHLIGHTERSTYLE09)

            self.Bind(stc.EVT_STC_DOUBLECLICK, self.OnSTCDoubleClick)

        def OnSTCDoubleClick(self, event):
            # Additional Code as Normal...
            event.Skip()
            print('do something else in addition to smart highlighting'
                  ' with out overiding the wx.stc.EVT_STC_DOUBLECLICK event.')


    class SmartHighlighterMixinPanel(wx.Panel):
        def __init__(self, parent, id=wx.ID_ANY,
                     pos=wx.DefaultPosition, size=wx.DefaultSize,
                     style=wx.BORDER_SUNKEN, name='panel'):
            wx.Panel.__init__(self, parent, id, pos, size, style, name)
            vbSizer = wx.BoxSizer(wx.VERTICAL)
            vbSizer.Add(PlainSTC(self), 1, wx.EXPAND | wx.ALL, 5)
            self.SetSizer(vbSizer)


    class SmartHighlighterMixinFrame(wx.Frame):
        def __init__(self, parent, id=wx.ID_ANY, title=wx.EmptyString,
                     pos=wx.DefaultPosition, size=wx.DefaultSize,
                     style=wx.DEFAULT_FRAME_STYLE, name='frame'):
            wx.Frame.__init__(self, parent, id, title, pos, size, style, name)
            panel = SmartHighlighterMixinPanel(self)
            self.Bind(wx.EVT_CLOSE, self.OnDestroy)
            wxVER = 'wxPython %s' % wx.version()
            pyVER = 'python %d.%d.%d.%s' % sys.version_info[0:4]
            versionInfos = '%s %s' % (wxVER, pyVER)
            self.CreateStatusBar().SetStatusText(versionInfos)

        def OnDestroy(self, event):
            self.Destroy()


    class SmartHighlighterMixinApp(wx.App):
        def OnInit(self):
            gMainWin = SmartHighlighterMixinFrame(None)
            gMainWin.SetTitle('StyledTextCtrl SmartHighlighterMixin Test')
            self.SetTopWindow(gMainWin)
            gMainWin.Show()
            return True


    gApp = SmartHighlighterMixinApp(redirect=False,
            filename=None,
            useBestVisual=False,
            clearSigInt=True)

    gApp.MainLoop()
