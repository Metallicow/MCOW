#!/usr/bin/env python
# -*- coding: utf-8 -*-


__wxPyDemoPanel__ = 'TestPanel'
#-Imports-----------------------------------------------------------------------

#--Python Imports.
import os
import sys
from collections import OrderedDict

#--wxPython Imports.
# import wxversion
# wxversion.select('2.8')
import wx
import wx.lib.scrolledpanel as scrolled
from wx.lib.gestures import MouseGestures

try:
    from mcow import threewaysplitter as TWS
except ImportError: # if it's not there locally, try the wxPython lib.
    import wx.lib.mcow.threewaysplitter as TWS

try: # Locally
    import mcow.shapedbitmapbutton as SBB
    from mcow.mixins.threewaysplitter import AnimMoveMouseGestureMixin
except ImportError: # wxPython library
    import wx.lib.mcow.shapedbitmapbutton as SBB
    from wx.lib.mcow.mixins.threewaysplitter import AnimMoveMouseGestureMixin

# import images

#-Globals-----------------------------------------------------------------------
try:
    gFileDir = os.path.dirname(os.path.abspath(__file__))
except:
    gFileDir = os.path.dirname(os.path.abspath(sys.argv[0]))
# sys.path.append(os.path.split(gFileDir)[0])

gBmpDir = gFileDir + os.sep + 'bitmaps'
gCurDir = gFileDir + os.sep + 'cursors'


DOUBLEBUFFERED = True


class SampleGradientPanel(wx.Panel, AnimMoveMouseGestureMixin):
    """
    Just a simple test window to put into the splitter.
    """
    def __init__(self, parent, gradColours, label):
        wx.Panel.__init__(self, parent, style=wx.BORDER_SUNKEN)
        self.parent = parent

        self.label = label
        self.gradColours = gradColours

        if 'Panel One' in label:
            self.pnxBmp = wx.Bitmap(gBmpDir + os.sep + 'phoenix128.png', wx.BITMAP_TYPE_PNG)

        if wx.VERSION_STRING.startswith('2.8.'):
            self.stLabel = wx.StaticText(self, -1, self.label, pos=(10, 10), style=wx.SIMPLE_BORDER)

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_MIDDLE_DCLICK, self.OnMiddleDClick)

        AnimMoveMouseGestureMixin.__init__(self)


    def OnMiddleDClick(self, event):
        self.parent.CenterSplittersWindows()

    def OnSize(self, event):
        self.Refresh()

    def OnPaint(self, event):
        tws = self.parent
        dc = wx.PaintDC(self) # More buffering will slow down the AnimationMoves.
        dc.GradientFillLinear(self.GetClientRect(),
                              self.gradColours[0], self.gradColours[1])
        # if 'Panel One' in self.label:
            # sz = self.GetSize()
            # twsSz = tws.GetSize()
            # gMainWin.SetTitle('Panel One Size = %s' % sz)
            # gMainWin.SetTitle('TWS Size = %s' % twsSz)

        winIndex = tws.GetWindowIndex(self)
        swap = winIndex + 1 # Add one for demo to show as one-based index
        if 'Panel One' in self.label:
            width, height = self.GetSize()
            dc.DrawBitmap(self.pnxBmp, width - 128 - 24, height - 128 - 24)
            self.label = ("Panel One - WinIndex %s - Swap %s" "\n\n"
                "There are three ways" "\n"
                "to drag sashes. Try" "\n"
                "dragging the horizontal" "\n"
                "sash, the vertical sash" "\n"
                "or position the mouse at" "\n"
                "the intersection of the" "\n"
                "two sashes."
                ) % (winIndex, swap)
        elif 'Panel Two' in self.label:
            self.label = ("Panel Two - WinIndex %s - Swap %s" "\n\n"
                "Try right clicking on the splitter" "\n"
                "to popup the default built-in menu!" "\n\n"
                "The middle mouse button double click event" "\n"
                "(wx.EVT_MIDDLE_DCLICK)" "\n"
                "has also been bound to the ThreeWaySplitter's" "\n"
                "CenterSplittersWindows function in this demo."
                ) % (winIndex, swap)
        elif 'Panel Three' in self.label:
             self.label = ("Panel Three - WinIndex %s - Swap %s" "\n\n"
                "In this demo, the ThreeWaySplitter's" "\n"
                "windows(children) make use of the" "\n"
                "AnimMoveMouseGestureMixin mixin." "\n\n"
                "Try doing some Mouse Gestures with" "\n"
                "the right mouse button." "\n\n"
                "AniMondrian! :)"
                ) % (winIndex, swap)

        dc.DrawText(self.label, 10, 10)

        event.Skip()


class ControlPane(scrolled.ScrolledPanel):

    def __init__(self, parent, size=wx.DefaultSize):

        self.parent = parent
        scrolled.ScrolledPanel.__init__(self, parent, size=size, style=wx.BORDER_SUNKEN)

        twsCl = 'ThreeWaySplitter'
        luCheck = wx.CheckBox(self, -1, "Live Update")
        luCheck.SetValue(True)
        self.Bind(wx.EVT_CHECKBOX, self.OnSetLiveUpdate, luCheck)

        ewST = wx.StaticText(self, -1, 'ExchangeWindows')
        ewST.SetToolTip(wx.ToolTip('%s.ExchangeWindows(window1, window2)' % twsCl))

        btn1 = wx.Button(self, -1, "Swap 1 && 2")
        self.Bind(wx.EVT_BUTTON, self.OnSwapButton12, btn1)

        btn2 = wx.Button(self, -1, "Swap 1 && 3")
        self.Bind(wx.EVT_BUTTON, self.OnSwapButton13, btn2)

        btn3 = wx.Button(self, -1, "Swap 2 && 3")
        self.Bind(wx.EVT_BUTTON, self.OnSwapButton23, btn3)

        loneSideST = wx.StaticText(self, -1, 'SetLoneSide')
        loneSideST.SetToolTip(wx.ToolTip('%s.SetLoneSide(side)' % twsCl))

        btn4 = wx.Button(self, -1, "wx.LEFT")
        btn4.SetToolTip(wx.ToolTip('%s.SetLoneSide(wx.LEFT)' % twsCl))
        self.Bind(wx.EVT_BUTTON, self.OnSetLoneSideLeft, btn4)

        btn5 = wx.Button(self, -1, "wx.TOP")
        btn5.SetToolTip(wx.ToolTip('%s.SetLoneSide(wx.TOP)' % twsCl))
        self.Bind(wx.EVT_BUTTON, self.OnSetLoneSideTop, btn5)

        btn6 = wx.Button(self, -1, "wx.RIGHT")
        btn6.SetToolTip(wx.ToolTip('%s.SetLoneSide(wx.RIGHT)' % twsCl))
        self.Bind(wx.EVT_BUTTON, self.OnSetLoneSideRight, btn6)

        btn7 = wx.Button(self, -1, "wx.BOTTOM")
        btn7.SetToolTip(wx.ToolTip('%s.SetLoneSide(wx.BOTTOM)' % twsCl))
        self.Bind(wx.EVT_BUTTON, self.OnSetLoneSideBottom, btn7)

        eawST = wx.StaticText(self, -1, "Expand A Window")
        eawST.SetToolTip(wx.ToolTip('%s.SetExpanded(expanded)' % twsCl))
        combo = wx.ComboBox(self, -1, choices=["None", "1", "2", "3"],
                            style=wx.CB_READONLY|wx.CB_DROPDOWN)
        combo.SetStringSelection("None")

        edcsCB = wx.CheckBox(self, -1, "DoubleClickSwitch")
        edcsCB.SetValue(True)
        edcsCB.Bind(wx.EVT_CHECKBOX, self.OnSetDoubleClickSwitch)

        self.Bind(wx.EVT_COMBOBOX, self.OnExpandWindow)

        self.spin1 = wx.SpinCtrl(self, -1, value='50', min=0, max=240, initial=50,
                                 style=wx.TE_PROCESS_ENTER)
        self.spin2 = wx.SpinCtrl(self, -1, value='50', min=0, max=240, initial=50,
                                 style=wx.TE_PROCESS_ENTER)
        self.spin1.Bind(wx.EVT_SPINCTRL, self.OnSpinCtrlX)
        self.spin1.Bind(wx.EVT_TEXT_ENTER, self.OnSpinCtrlX)
        self.spin1.Bind(wx.EVT_TEXT, self.OnSpinCtrlX)
        self.spin2.Bind(wx.EVT_SPINCTRL, self.OnSpinCtrlY)
        self.spin2.Bind(wx.EVT_TEXT_ENTER, self.OnSpinCtrlY)
        self.spin2.Bind(wx.EVT_TEXT, self.OnSpinCtrlY)

        animST = wx.StaticText(self, -1, 'AnimatedMove')
        animST.SetToolTip(wx.ToolTip('%s.AnimatedMove(splitterAnimDirection)' % twsCl))

        btn8 = wx.Button(self, -1, "wx.LEFT\nor\nwx.WEST")
        try:
            btn8.SetBitmap(wx.Bitmap(gBmpDir + os.sep + 'arrow_left_16.png', wx.BITMAP_TYPE_PNG))
        except AttributeError: # wx28
            pass
        btn8.SetToolTip(wx.ToolTip("%s.AnimatedMove(wx.LEFT)\n"
                                   "or\n"
                                   "%s.AnimatedMove(wx.WEST)" %(twsCl, twsCl)))
        self.Bind(wx.EVT_BUTTON, parent.p1.AnimLeft, btn8)

        btn9 = wx.Button(self, -1, "wx.TOP\nor\nwx.NORTH")
        try:
            btn9.SetBitmap(wx.Bitmap(gBmpDir + os.sep + 'arrow_up_16.png', wx.BITMAP_TYPE_PNG))
        except AttributeError: # wx28
            pass
        btn9.SetToolTip(wx.ToolTip("%s.AnimatedMove(wx.TOP)\n"
                                   "or\n"
                                   "%s.AnimatedMove(wx.NORTH)" %(twsCl, twsCl)))
        self.Bind(wx.EVT_BUTTON, parent.p1.AnimTop, btn9)

        btn10 = wx.Button(self, -1, "wx.RIGHT\nor\nwx.EAST")
        try:
            btn10.SetBitmap(wx.Bitmap(gBmpDir + os.sep + 'arrow_right_16.png', wx.BITMAP_TYPE_PNG))
        except AttributeError: # wx28
            pass
        btn10.SetToolTip(wx.ToolTip("%s.AnimatedMove(wx.RIGHT)\n"
                                   "or\n"
                                   "%s.AnimatedMove(wx.EAST)" %(twsCl, twsCl)))
        self.Bind(wx.EVT_BUTTON, parent.p1.AnimRight, btn10)

        btn11 = wx.Button(self, -1, "wx.BOTTOM\nor\nwx.SOUTH")
        try:
            btn11.SetBitmap(wx.Bitmap(gBmpDir + os.sep + 'arrow_down_16.png', wx.BITMAP_TYPE_PNG))
        except AttributeError: # wx28
            pass
        btn11.SetToolTip(wx.ToolTip("%s.AnimatedMove(wx.BOTTOM)\n"
                                   "or\n"
                                   "%s.AnimatedMove(wx.SOUTH)" %(twsCl, twsCl)))
        self.Bind(wx.EVT_BUTTON, parent.p1.AnimBottom, btn11)

        btn12 = wx.Button(self, -1, "wx.TOP | wx.LEFT\nor\nwx.NORTH | wx.WEST")
        try:
            btn12.SetBitmap(wx.Bitmap(gBmpDir + os.sep + 'arrow_upleft_16.png', wx.BITMAP_TYPE_PNG))
        except AttributeError: # wx28
            pass
        btn12.SetToolTip(wx.ToolTip("%s.AnimatedMove(wx.TOP | wx.LEFT)\n"
                                   "or\n"
                                   "%s.AnimatedMove(wx.NORTH | wx.WEST)" %(twsCl, twsCl)))
        self.Bind(wx.EVT_BUTTON, parent.p1.AnimTopLeft, btn12)

        btn13 = wx.Button(self, -1, "wx.TOP | wx.RIGHT\nor\nwx.NORTH | wx.EAST")
        try:
            btn13.SetBitmap(wx.Bitmap(gBmpDir + os.sep + 'arrow_upright_16.png', wx.BITMAP_TYPE_PNG))
        except AttributeError: # wx28
            pass
        btn13.SetToolTip(wx.ToolTip("%s.AnimatedMove(wx.TOP | wx.RIGHT)\n"
                                   "or\n"
                                   "%s.AnimatedMove(wx.NORTH | wx.EAST)" %(twsCl, twsCl)))
        self.Bind(wx.EVT_BUTTON, parent.p1.AnimTopRight, btn13)

        btn14 = wx.Button(self, -1, "wx.BOTTOM | wx.LEFT\nor\nwx.SOUTH | wx.WEST")
        try:
            btn14.SetBitmap(wx.Bitmap(gBmpDir + os.sep + 'arrow_downleft_16.png', wx.BITMAP_TYPE_PNG))
        except AttributeError: # wx28
            pass
        btn14.SetToolTip(wx.ToolTip("%s.AnimatedMove(wx.BOTTOM | wx.LEFT)\n"
                                   "or\n"
                                   "%s.AnimatedMove(wx.SOUTH | wx.WEST)" %(twsCl, twsCl)))
        self.Bind(wx.EVT_BUTTON, parent.p1.AnimBottomLeft, btn14)

        btn15 = wx.Button(self, -1, "wx.BOTTOM | wx.RIGHT\nor\nwx.SOUTH | wx.EAST")
        try:
            btn15.SetBitmap(wx.Bitmap(gBmpDir + os.sep + 'arrow_downright_16.png', wx.BITMAP_TYPE_PNG))
        except AttributeError: # wx28
            pass
        btn15.SetToolTip(wx.ToolTip("%s.AnimatedMove(wx.BOTTOM | wx.RIGHT)\n"
                                   "or\n"
                                   "%s.AnimatedMove(wx.SOUTH | wx.EAST)" %(twsCl, twsCl)))
        self.Bind(wx.EVT_BUTTON, parent.p1.AnimBottomRight, btn15)

        if wx.VERSION_STRING.startswith('2.8.'):
            useCustomCursors = wx.CheckBox(self, -1, "Use Custom Cursors")
            useCustomCursors.Bind(wx.EVT_CHECKBOX, self.OnSetSplitterCursors)
        else:
            try:
                useCustomCursors = wx.ToggleButton(self, -1, "Use Custom Cursors")
                useCustomCursors.SetBitmap(wx.Bitmap(gCurDir + os.sep + 'paperairplane_sizing_dark.png', wx.BITMAP_TYPE_PNG))
                useCustomCursors.Bind(wx.EVT_TOGGLEBUTTON, self.OnSetSplitterCursors)
            except AttributeError:
                useCustomCursors = wx.CheckBox(self, -1, "Use Custom Cursors")
                useCustomCursors.Bind(wx.EVT_CHECKBOX, self.OnSetSplitterCursors)

        savePerspBtn = wx.Button(self, -1, "SavePerspective")
        savePerspBtn.Bind(wx.EVT_BUTTON, self.OnSavePerspective)

        self.loadPerspBtn = wx.Button(self, -1, "LoadPerspective")
        self.loadPerspBtn.Bind(wx.EVT_BUTTON, self.OnLoadPerspective)
        self.loadPerspBtn.Enable(False)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(luCheck, 0, wx.TOP, 5)
        sizer.Add(wx.StaticLine(self, size=(-1, 1)), 0, wx.EXPAND | wx.TOP, 5)
        sizer.Add(ewST, 0, wx.TOP, 5)
        sizer.Add(btn1, 0, wx.TOP, 5)
        sizer.Add(btn2, 0, wx.TOP, 5)
        sizer.Add(btn3, 0, wx.TOP, 5)
        sizer.Add(wx.StaticLine(self, size=(-1, 1)), 0, wx.EXPAND | wx.TOP, 5)
        sizer.Add(eawST, 0, wx.TOP, 10)
        sizer.Add(combo, 0, wx.EXPAND | wx.RIGHT | wx.TOP, 5)
        sizer.Add(wx.StaticLine(self, size=(-1, 1)), 0, wx.EXPAND | wx.TOP, 5)
        sizer.Add(loneSideST, 0, wx.TOP, 5)
        sizer.Add(btn4, 0, wx.TOP, 5)
        sizer.Add(btn5, 0, wx.TOP, 5)
        sizer.Add(btn6, 0, wx.TOP, 5)
        sizer.Add(btn7, 0, wx.TOP, 5)
        sizer.Add(wx.StaticLine(self, size=(-1, 1)), 0, wx.EXPAND | wx.TOP, 5)
        sizer.Add(edcsCB, 0, wx.TOP, 5)

        self.modCBs = []
        for i in dir(wx):
            if i.startswith('MOD_'):
                modCB = wx.CheckBox(self, -1, "wx.%s" % i)
                if i == 'MOD_NONE':
                    modCB.SetValue(True)
                    modCB.Enable(False)
                elif i == 'MOD_ALL':
                    humorTT = ( # lets poke some fun at all the folks that will actually try this one...
                        "If you can manage to get this to fire off...," "\n"
                        "then chances are that you are a 3 armed mutant" "\n"
                        "alien with eight 8 inch fingers on all hands," "\n"
                        "and your name is probably `Steve Vai` and also have" "\n"
                        "guru shredding abilities like `Mr.Fastfinger`." "\n"
                        ":)")
                    modCB.SetToolTip(wx.ToolTip(humorTT))
                modCB.Bind(wx.EVT_CHECKBOX, self.OnSetDoubleClickSwitchModifiers)
                sizer.Add(modCB, 0, wx.TOP, 5)
                self.modCBs.append(modCB)
                # print(i)

        sizer.Add(wx.StaticLine(self, size=(-1, 1)), 0, wx.EXPAND | wx.TOP, 5)
        sizer.Add(wx.StaticText(self, -1, 'SetMinimumSizeX'), 0, wx.TOP, 5)
        sizer.Add(self.spin1, 0, wx.TOP, 5)
        sizer.Add(wx.StaticText(self, -1, 'SetMinimumSizeY'), 0, wx.TOP, 5)
        sizer.Add(self.spin2, 0, wx.TOP, 5)

        sizer.Add(wx.StaticLine(self, size=(-1, 1)), 0, wx.EXPAND | wx.TOP, 5)
        sizer.Add(animST, 0, wx.TOP, 5)
        sizer.Add(btn8, 0, wx.TOP, 5)
        sizer.Add(btn9, 0, wx.TOP, 5)
        sizer.Add(btn10, 0, wx.TOP, 5)
        sizer.Add(btn11, 0, wx.TOP, 5)
        sizer.Add(btn12, 0, wx.TOP, 5)
        sizer.Add(btn13, 0, wx.TOP, 5)
        sizer.Add(btn14, 0, wx.TOP, 5)
        sizer.Add(btn15, 0, wx.TOP, 5)

        sizer.Add(wx.StaticLine(self, size=(-1, 1)), 0, wx.EXPAND | wx.TOP, 5)
        sizer.Add(wx.StaticText(self, -1, 'SetSplitterCursors'), 0, wx.TOP, 5)
        sizer.Add(useCustomCursors, 0, wx.TOP, 5)

        sizer.Add(wx.StaticLine(self, size=(-1, 1)), 0, wx.EXPAND | wx.TOP, 5)
        sizer.Add(savePerspBtn, 0, wx.TOP, 5)
        sizer.Add(self.loadPerspBtn, 0, wx.TOP, 5)

        border = wx.BoxSizer()
        border.Add(sizer, 1, wx.EXPAND | wx.ALL, 5)
        self.SetSizer(border)

        self.SetupScrolling()


    def OnSavePerspective(self, event):
        self.savedPerspectiveStr = self.GetParent().splitter.SavePerspective()
        if not self.loadPerspBtn.IsEnabled():
            self.loadPerspBtn.Enable(True)

    def OnLoadPerspective(self, event):
        if self.savedPerspectiveStr: # Make sure we have something there.
            self.GetParent().splitter.LoadPerspective(self.savedPerspectiveStr)

    def OnSetSplitterCursors(self, event):
        isChecked = event.GetEventObject().GetValue()
        curBoth = wx.Image(gCurDir + os.sep + 'paperairplane_sizing_dark.png', wx.BITMAP_TYPE_PNG)
        curHor = wx.Image(gCurDir + os.sep + 'paperairplane_sizewe_dark.png', wx.BITMAP_TYPE_PNG)
        curVer = wx.Image(gCurDir + os.sep + 'paperairplane_sizens_dark.png', wx.BITMAP_TYPE_PNG)
        for cur in (curBoth, curHor, curVer):
            try:
                cur.SetOption(wx.IMAGE_OPTION_CUR_HOTSPOT_X, 15)
                cur.SetOption(wx.IMAGE_OPTION_CUR_HOTSPOT_Y, 15)
            except TypeError:
                cur.SetOption('wx.IMAGE_OPTION_CUR_HOTSPOT_X', '15')
                cur.SetOption('wx.IMAGE_OPTION_CUR_HOTSPOT_Y', '15')
        if isChecked: # Set them to our custom cursors.
            try:
                self.GetParent().splitter.SetSplitterCursors(
                    cursorBOTH=wx.Cursor(curBoth),
                    cursorHORIZONTAL=wx.Cursor(curHor),
                    cursorVERTICAL=wx.Cursor(curVer))
            except TypeError: # wx28
                self.GetParent().splitter.SetSplitterCursors(
                    cursorBOTH=wx.Cursor(gCurDir + os.sep + 'paperairplane_sizing_dark.cur', wx.BITMAP_TYPE_CUR),
                    cursorHORIZONTAL=wx.Cursor(gCurDir + os.sep + 'paperairplane_sizewe_dark.cur', wx.BITMAP_TYPE_CUR),
                    cursorVERTICAL=wx.Cursor(gCurDir + os.sep + 'paperairplane_sizens_dark.cur', wx.BITMAP_TYPE_CUR))
        else: # Set them to default system cursors.
            self.GetParent().splitter.SetSplitterCursors()

    def OnSpinCtrlX(self, event=None):
        # print(event.GetInt())
        self.GetParent().splitter.SetMinimumSizeX(self.spin1.GetValue())
        self.GetParent().splitter.SendSizeEvent()

    def OnSpinCtrlY(self, event=None):
        # print(event.GetInt())
        self.GetParent().splitter.SetMinimumSizeY(self.spin2.GetValue())
        self.GetParent().splitter.SendSizeEvent()

    def OnSetDoubleClickSwitchModifiers(self, event):
        modifiers = wx.MOD_NONE
        for checkbox in self.modCBs:
            # print('%s, %s' %(checkbox.GetLabel(), checkbox.GetValue()))
            if checkbox.GetValue():
                modifiers |= eval(checkbox.GetLabel())
        self.GetParent().splitter.SetDoubleClickSwitchModifiers(modifiers)
        # print('-' * 30)

    def OnSetDoubleClickSwitch(self, event):
        self.GetParent().splitter.EnableDoubleClickSwitch(event.GetInt())

    def OnSetLoneSideLeft(self, event):
        self.GetParent().splitter.SetLoneSide(wx.LEFT)

    def OnSetLoneSideTop(self, event):
        self.GetParent().splitter.SetLoneSide(wx.TOP)

    def OnSetLoneSideRight(self, event):
        self.GetParent().splitter.SetLoneSide(wx.RIGHT)

    def OnSetLoneSideBottom(self, event):
        self.GetParent().splitter.SetLoneSide(wx.BOTTOM)

    def OnSetLiveUpdate(self, event):
        check = event.GetEventObject()
        self.GetParent().SetLiveUpdate(check.GetValue())

    def OnSwapButton12(self, event):
        self.GetParent().Swap1and2()

    def OnSwapButton13(self, event):
        self.GetParent().Swap1and3()

    def OnSwapButton23(self, event):
        self.GetParent().Swap2and3()

    def OnExpandWindow(self, event):
        self.GetParent().ExpandWindow(event.GetSelection())


class TWSDemoPanel(wx.Panel):

    def __init__(self, parent, log):

        wx.Panel.__init__(self, parent, -1)
        self.log = log
        self.parent = parent

        splitter = TWS.ThreeWaySplitter(self, agwStyle=wx.SP_LIVE_UPDATE, loneSide=wx.TOP)
        # splitter.SetDoubleBuffered(True) # Reduce gradient flicker.
        if DOUBLEBUFFERED:
            splitter.SetDoubleBuffered(True) # Reduce gradient flicker on moving splitter.

        self.splitter = splitter
        self.log = log

        self.p1 = SampleGradientPanel(splitter, ("#DAA520", "#FFFFFF"), "Panel One") # goldenrod
        splitter.AppendWindow(self.p1)

        self.p2 = SampleGradientPanel(splitter, ("#CD5C5C", "#FFFFFF"), "Panel Two") # indianred
        splitter.AppendWindow(self.p2)

        self.p3 = SampleGradientPanel(splitter, ("#3A5FCD", "#FFFFFF"), "Panel Three") # royalblue3
        # from ShapedBitmapButton_Tiled_HWrapSizer import ShapedBitmapButtonPanel0
        # from ShapedBitmapButton import ShapedBitmapButtonPanel2
        # self.p3 = ShapedBitmapButtonPanel2(splitter)
        splitter.AppendWindow(self.p3)
        splitter.SetWindowsPopupLabels("Panel One", "Panel Two", "Panel Three")

        try:
            self.log.write("Welcome to the ThreeWaySplitterDemo!\n")
        except AttributeError: # running from __main__.
            pass

        self.controlPane = ControlPane(self, size=(250, -1))

        self.Bind(wx.EVT_SPLITTER_SASH_POS_CHANGED, self.OnChanged)
        self.Bind(wx.EVT_SPLITTER_SASH_POS_CHANGING, self.OnChanging)

        # splitter.SetSashTrackerPen(pen=wx.Pen(wx.RED, 2, wx.PENSTYLE_CROSS_HATCH))

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(self.controlPane, 0, wx.EXPAND | wx.ALL)
        sizer.Add(splitter, 1, wx.EXPAND)
        self.SetSizer(sizer)
        self.Fit()

    def GetSashIdx(self, event):
        if event.GetSashIdx() == wx.HORIZONTAL:
            idx = "Horizontal"
        elif event.GetSashIdx() == wx.VERTICAL:
            idx = "Vertical"
        else:
            idx = "Horizontal & Vertical"

        return idx

    def OnChanging(self, event):
        idx = self.GetSashIdx(event)
        dPrint = "Changing sash: %s  %s\n" %(idx, event.GetSashPosition())
        try:
            self.log.write(dPrint)
        except AttributeError: # running from __main__.
            print(dPrint)

        # This is one way to control the sash limits
        #if event.GetSashPosition().x < 50:
        #    event.Veto()

        event.Skip()

    def OnChanged(self, event):
        idx = self.GetSashIdx(event)
        dPrint = "Changed sash: %s  %s\n" %(idx, event.GetSashPosition())
        try:
            self.log.write(dPrint)
        except AttributeError: # running from __main__.
            print(dPrint)

        event.Skip()

    def SetLiveUpdate(self, enable):
        if enable:
            self.splitter.SetAGWWindowStyleFlag(wx.SP_LIVE_UPDATE)
        else:
            self.splitter.SetAGWWindowStyleFlag(0)

    def Swap1and2(self):
        win1 = self.splitter.GetWindow(0)
        win2 = self.splitter.GetWindow(1)
        self.splitter.ExchangeWindows(win1, win2)

    def Swap1and3(self):
        win1 = self.splitter.GetWindow(0)
        win3 = self.splitter.GetWindow(2)
        self.splitter.ExchangeWindows(win1, win3)

    def Swap2and3(self):
        win2 = self.splitter.GetWindow(1)
        win3 = self.splitter.GetWindow(2)
        self.splitter.ExchangeWindows(win2, win3)

    def ExpandWindow(self, selection):
        self.splitter.SetExpanded(selection-1)


class ThreeWaySplitterDemo(wx.Frame):

    def __init__(self, parent, log, id=wx.ID_ANY,
                 title="ThreeWaySplitter Demo",
                 pos=wx.DefaultPosition, size=wx.DefaultSize):

        wx.Frame.__init__(self, parent, id, title, pos, size)

        global gMainWin
        gMainWin = self

        self.log = log
        ## if DOUBLEBUFFERED:
        ##     self.SetDoubleBuffered(True) # Reduce gradient flicker on size.
        self.panel = TWSDemoPanel(self, log)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.panel, 1, wx.EXPAND)
        self.SetSizer(sizer)
        sizer.Layout()

        try:
            statusbar = self.CreateStatusBar(2, wx.ST_SIZEGRIP)
        except AttributeError:
            statusbar = self.CreateStatusBar(2, wx.STB_SIZEGRIP)

        statusbar.SetStatusWidths([-2, -1])
        # statusbar fields
        statusbar_fields = [("ThreeWaySplitter wxPython Demo, (c) Edward Greig @ 13 Jan 2014"),
                            ("wxPython %s" % wx.version())]

        for i in range(len(statusbar_fields)):
            statusbar.SetStatusText(statusbar_fields[i], i)

        self.CreateMenu()

        # self.SetIcon(images.Mondrian.GetIcon())
        self.CenterOnScreen()

        # Update the MinimumSize Immediately.
        self.panel.controlPane.OnSpinCtrlX()
        self.panel.controlPane.OnSpinCtrlY()

    def CreateMenu(self):

        menuBar = wx.MenuBar(wx.MB_DOCKABLE)
        fileMenu = wx.Menu()
        helpMenu = wx.Menu()

        fileMenu.Append(wx.ID_CLOSE, "E&xit")
        self.Bind(wx.EVT_MENU, self.OnQuit, id=wx.ID_CLOSE)

        helpMenu.Append(wx.ID_ABOUT, "About")
        self.Bind(wx.EVT_MENU, self.OnAbout, id=wx.ID_ABOUT)

        menuBar.Append(fileMenu, "&File")
        menuBar.Append(helpMenu, "&Help")

        self.SetMenuBar(menuBar)


    def OnQuit(self, event):

        self.Destroy()


    def OnAbout(self, event):

        msg = ("This Is The About Dialog Of The ThreeWaySplitter Demo.\n\n"
                "Authors:\n"
                "Andrea Gavana @ 03 Nov 2006 - FourWaySplitter\n"
                "Edward Greig, @ 13 Jan 2014 - ThreeWaySplitter\n\n"
                "Please Report Any Bug/Requests Of Improvements\n"
                "To Us At The Following Addresses:\n\n"
                "andrea.gavana@gmail.com\n" + "andrea.gavana@maerskoil.com\n"
                "or\n"
                "metaliobovinus@gmail.com\n\n"
                "Welcome To wxPython " + wx.VERSION_STRING + "!!")

        dlg = wx.MessageDialog(self, msg, "ThreeWaySplitter wxPython Demo",
                               wx.OK | wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()


# wxPy Demo ------------------------------------------------------------------


class TestPanel(wx.Panel):
    def __init__(self, parent, log):
        self.log = log
        wx.Panel.__init__(self, parent, -1)

        b = wx.Button(self, -1, "Show the ThreeWaySplitter Demo", (50,50))
        self.Bind(wx.EVT_BUTTON, self.OnButton, b)


    def OnButton(self, event):
        dSz = wx.GetDisplaySize()
        halfW, halfH = int(dSz[0]/2), int(dSz[1]/2) + int(dSz[1]/6)
        minSzW, minSzY = 700, 500
        w = minSzW if minSzW > halfW else halfW
        h = minSzY if minSzY > halfH else halfH
        self.win = ThreeWaySplitterDemo(self, self.log, size=(w, h))
        self.win.Show(True)


def runTest(frame, nb, log):
    win = TestPanel(nb, log)
    return win

overview = TWS.__doc__


# __main__ Demo --------------------------------------------------------------


class TestApp(wx.App):
    def OnInit(self):
        dSz = wx.GetDisplaySize()
        halfW, halfH = int(dSz[0]/2), int(dSz[1]/2) + int(dSz[1]/6)
        minSzW, minSzY = 700, 500
        w = minSzW if minSzW > halfW else halfW
        h = minSzY if minSzY > halfH else halfH
        frame = ThreeWaySplitterDemo(None, -1, size=(w, h))
        # frame.SetIcon(application16.GetIcon())
        self.SetTopWindow(frame)
        frame.Show()
        self.SetAppName("ThreeWaySplitter Demo")

        return True


if __name__ == '__main__':
    app = TestApp(redirect=False,
                  filename=None,
                  useBestVisual=False,
                  clearSigInt=True)
    app.MainLoop()
