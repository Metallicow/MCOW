#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
animation.py
============

Animation functions.

TODOs:
------
1. Make an alternate SmoothMultiMove from SmoothMove that takes iterables for
   its params so as to move multiple widgets at the same time.

"""

# Imports.--------------------------------------------------------------------

# -wxPython Imports.
import wx


def SmoothMove(windo, moveToPos, animStep=42):
    """
    Animate moving a widget to a position

    :param `windo`: A window to smoothly movely
    :type `windo`: `wx.Window`
    :param `moveToPos`: A point to move the windo to
    :type `moveToPos`: `wx.Point`
    :param `animStep`: Number of steps per iteration. Higher numbers animate slower but smoother.
     Must not be lower than 6. The number will be converted to float anyways.
    :type `animStep`: int or float
    """
    windoPosX, windoPosY = xStart, yStart = windo.GetPosition()
    moveToPosX, moveToPosY = moveToPos

    animStep = float(animStep)  # We must make a float
    if animStep < 6.0:
        animStep = 6.0
    step = animStep/3

    xStep = int((windoPosX - moveToPosX))/step
    yStep = int((windoPosY - moveToPosY))/step

    wxMilliSleep = wx.MilliSleep
    windo_Move = windo.Move
    windo_Update = windo.Update
    windo_GetPosition = windo.GetPosition

    for i in range(int(step)):
        windoX, windoY = windo_GetPosition()
        if ((windoX == moveToPosX and windoY == moveToPosY)
             or ((windoX + 1 == moveToPosX) and (windoY + 1 == moveToPosY))
             or ((windoX - 1 == moveToPosX) and (windoY - 1 == moveToPosY))
             or ((windoX + 1 == moveToPosX) and (windoY - 1 == moveToPosY))
             or ((windoX - 1 == moveToPosX) and (windoY + 1 == moveToPosY))
             or ((windoX == moveToPosX) and (windoY + 1 == moveToPosY))
             or ((windoX == moveToPosX) and (windoY - 1 == moveToPosY))
             or ((windoX + 1 == moveToPosX) and (windoY == moveToPosY))
             or ((windoX - 1 == moveToPosX) and (windoY == moveToPosY))
            ):
            windo_Move((moveToPosX, moveToPosY))
            windo_Update()
            break
        windo_Move((xStart - i*xStep, yStart - i*yStep))
        windo_Update()
        wxMilliSleep(10)

    windoX, windoY = windo_GetPosition()
    print(windo_GetPosition(), moveToPos)
    if ((windoX == moveToPosX and windoY == moveToPosY)
         or ((windoX + 1 == moveToPosX) and (windoY + 1 == moveToPosY))
         or ((windoX - 1 == moveToPosX) and (windoY - 1 == moveToPosY))
         or ((windoX + 1 == moveToPosX) and (windoY - 1 == moveToPosY))
         or ((windoX - 1 == moveToPosX) and (windoY + 1 == moveToPosY))
         or ((windoX == moveToPosX) and (windoY + 1 == moveToPosY))
         or ((windoX == moveToPosX) and (windoY - 1 == moveToPosY))
         or ((windoX + 1 == moveToPosX) and (windoY == moveToPosY))
         or ((windoX - 1 == moveToPosX) and (windoY == moveToPosY))
         ):
        windo_Move((moveToPosX, moveToPosY))
        windo_Update()
        return
    else:  # Loop until we get there...
        SmoothMove(windo, moveToPos, animStep)


def SmoothMultiMove(windoList, moveToPosList, animStepList):
    """
    Animate moving multiple widgets to positions all at the same time, not in order

    :param `windoList`: A window to smoothly movely
    :type `windoList`: `wx.Window`
    :param `moveToPosList`: A point to move the windo to
    :type `moveToPosList`: `wx.Point`
    :param `animStepList`: Number of steps per iteration. Higher numbers animate slower but smoother.
     Must not be lower than 6. The number will be converted to float anyways.
    :type `animStepList`: int or float
    """
    if not len(windoList) == len(moveToPosList) == len(animStepList):
        raise Exception('windoList, moveToPosList, and animStepList MUST all have the same number of items!')
    lenAllLists = len(windoList)

    windoPosXList = []
    windoPosYList = []
    xStartList = []
    yStartList = []
    for windo in windoList:
        windoPosX, windoPosY = xStart, yStart = windo.GetPosition()
        windoPosXList.append(windoPosX)
        windoPosYList.append(windoPosY)
        xStartList.append(xStart)
        yStartList.append(yStart)

    moveToPosXList = []
    moveToPosYList = []
    for moveToPos in moveToPosList:
        moveToPosX, moveToPosY = moveToPos
        moveToPosXList.append(moveToPosX)
        moveToPosYList.append(moveToPosY)

    stepList = []
    for animStep in animStepList:
        aniStep = float(animStep)  # We must make a float
        if aniStep < 6.0:
            aniStep = 6.0
        step = aniStep/3
        stepList.append(step)

    xStepList = []
    yStepList = []
    for i in range(lenAllLists):
        xStep = int((windoPosXList[i] - moveToPosXList[i]))/stepList[i]
        yStep = int((windoPosYList[i] - moveToPosYList[i]))/stepList[i]
        xStepList.append(xStep)
        yStepList.append(yStep)

    # Local opts
    wxMilliSleep = wx.MilliSleep
    windo_MoveList = []
    windo_UpdateList = []
    windo_GetPositionList = []
    for windo in windoList:
        windo_Move = windo.Move
        windo_Update = windo.Update
        windo_GetPosition = windo.GetPosition
        windo_MoveList.append(windo_Move)
        windo_UpdateList.append(windo_Update)
        windo_GetPositionList.append(windo_GetPosition)

    # Example zip: [(windo#,  moveToPosX#,  moveToPosY#, animStep#), etc...]
    multiZip = zip(windoList, moveToPosXList, moveToPosYList, animStepList, windo_MoveList, windo_UpdateList, windo_GetPositionList, xStartList, yStartList, xStepList, yStepList)

    ##ii = 0
    ##multiZip1 = [z for z in multiZip]  # Copy it.
    for window, moveToPosX, moveToPosY, step, windo_Move, windo_Update, windo_GetPosition, xStart, yStart, xStep, yStep in multiZip:
        for i in range(int(step)):  # step
            windoX, windoY = windo_GetPosition()
            if ((windoX == moveToPosX and windoY == moveToPosY)
                 or ((windoX + 1 == moveToPosX) and (windoY + 1 == moveToPosY))
                 or ((windoX - 1 == moveToPosX) and (windoY - 1 == moveToPosY))
                 or ((windoX + 1 == moveToPosX) and (windoY - 1 == moveToPosY))
                 or ((windoX - 1 == moveToPosX) and (windoY + 1 == moveToPosY))
                 or ((windoX == moveToPosX) and (windoY + 1 == moveToPosY))
                 or ((windoX == moveToPosX) and (windoY - 1 == moveToPosY))
                 or ((windoX + 1 == moveToPosX) and (windoY == moveToPosY))
                 or ((windoX - 1 == moveToPosX) and (windoY == moveToPosY))
                ):
                windo_Move((moveToPosX, moveToPosY))
                windo_Update()
                break
            windo_Move((xStart - i*xStep, yStart - i*yStep))
            windo_Update()
            wxMilliSleep(10)

    # ii = 0
    removeTheseList = []
    for window, moveToPosX, moveToPosY, step, windo_Move, windo_Update, windo_GetPosition, xStart, yStart, xStep, yStep in multiZip:
        windoX, windoY = windo_GetPosition()
        # print(windo_GetPosition(), moveToPos)
        if ((windoX == moveToPosX and windoY == moveToPosY)
             or ((windoX + 1 == moveToPosX) and (windoY + 1 == moveToPosY))
             or ((windoX - 1 == moveToPosX) and (windoY - 1 == moveToPosY))
             or ((windoX + 1 == moveToPosX) and (windoY - 1 == moveToPosY))
             or ((windoX - 1 == moveToPosX) and (windoY + 1 == moveToPosY))
             or ((windoX == moveToPosX) and (windoY + 1 == moveToPosY))
             or ((windoX == moveToPosX) and (windoY - 1 == moveToPosY))
             or ((windoX + 1 == moveToPosX) and (windoY == moveToPosY))
             or ((windoX - 1 == moveToPosX) and (windoY == moveToPosY))
             ):
            windo_Move((moveToPosX, moveToPosY))
            windo_Update()
            this = (window, moveToPosX, moveToPosY, step, windo_Move, windo_Update, windo_GetPosition, xStart, yStart, xStep, yStep)
            removeTheseList.append(this)
            # ii = ii + 1
            # return

    for this in removeTheseList:
        multiZip.remove(this)

    if multiZip:
        # Unzip the list.
        windoList, moveToPosXList, moveToPosYList, animStepList, windo_MoveList, windo_UpdateList, windo_GetPositionList, xStartList, yStartList, xStepList, yStepList = zip(*multiZip)
        # Loop until we get there...
        SmoothMultiMove(windoList, moveToPosList, animStepList)


if __name__ == '__main__':
    import sys
    import wx
    from threading import Thread, Event


    import  wx.lib.newevent
    # This creates a new Event class and a EVT binder function
    (UpdateSmoothMoveEvent, EVT_UPDATE_SMOOTHMOVE) = wx.lib.newevent.NewEvent()

    class SmoothThreadMove(Thread):
        """Non Blocking Thread"""
        def __init__(self, event, windo, moveToPos, animStep):
            """Default class constructor."""
            Thread.__init__(self)

            self.windo = windo
            self.moveToPos = moveToPos
            self.animStep = animStep
            self.stopTimer = event

        def run(self):
            """Run the Thread."""
            SmoothMove(self.windo, self.moveToPos, self.animStep)

        def stop(self):
            """Stop the Thread."""
            self.stopTimer.set()
            print('stop')

        def stopped(self):
            """Is the Thread stopped?"""
            return self.stopTimer.isSet()
            print('stopped')

    class AnimationTestPanel1(wx.Panel):
        """SmoothMove Testing"""
        def __init__(self, parent):
            wx.Panel.__init__(self, parent, -1)

            self.ctrl = wx.Button(self, -1, "Click on me to hide me\nor\nclick on the background to move me", (50, 50))
            self.ctrl.Bind(wx.EVT_BUTTON, self.OnButton)
            self.Bind(wx.EVT_LEFT_UP, self.AnimatedMoveCtrlToPos)

        def OnButton(self, event):
            # Move off screen.
            w, h = self.ctrl.GetSize()
            SmoothMove(self.ctrl, moveToPos=(-1 - w, -1 - h))
            print('OnButton')

        def AnimatedMoveCtrlToPos(self, event=None):
            SmoothMove(self.ctrl, moveToPos=event.GetPosition())
            print('OnLeftUp')

    class AnimationTestPanel2(wx.Panel):
        """SmoothMultiMove Testing"""
        def __init__(self, parent):
            wx.Panel.__init__(self, parent, -1)

            self.ctrl0 = wx.Button(self, -1, "Smooth", (50, 50))
            self.ctrl1 = wx.Button(self, -1, "Multi", (225, 350))
            self.ctrl2 = wx.Button(self, -1, "Move", (450, 50))
            self.ctrl3 = wx.StaticText(self, -1, "Left or Right Click\non background", pos=(250, 150), style=wx.BORDER)

            self.Bind(wx.EVT_BUTTON, self.OnButton)
            self.Bind(wx.EVT_LEFT_UP, self.AnimatedMultiMoveCtrlsToPos)
            self.Bind(wx.EVT_RIGHT_UP, self.AnimatedMultiMoveCtrlsToPos2)

        def OnButton(self, event):
            print(event.GetEventObject().GetLabel())

        def AnimatedMultiMoveCtrlsToPos(self, event=None):
            windoList = [self.ctrl0, self.ctrl1, self.ctrl2]
            moveToPosList = [(100, 350), (225, 50), (400, 350)]
            animStepList = [42, 42, 42]
            SmoothMultiMove(windoList, moveToPosList, animStepList)
            print('OnLeftUp')

        def AnimatedMultiMoveCtrlsToPos2(self, event=None):
            windoList = [self.ctrl0, self.ctrl1, self.ctrl2]
            moveToPosList = [(50, 50), (225, 350), (450, 50)]
            animStepList = [420, 420, 420]
            SmoothMultiMove(windoList, moveToPosList, animStepList)
            print('OnRightUp')

    class AnimationTestPanel3(wx.Panel):
        """SmoothThreadMove Testing"""
        def __init__(self, parent):
            wx.Panel.__init__(self, parent, -1)

            self.SetDoubleBuffered(True)
            self.ctrl0 = wx.Button(self, -1, "Smooth", pos=(50, 50), size=(100, -1))
            self.ctrl1 = wx.Button(self, -1, "Thread", pos=(250, 350), size=(100, -1))
            self.ctrl2 = wx.Button(self, -1, "Move", pos=(450, 50), size=(100, -1))
            self.ctrl3 = wx.StaticText(self, -1, "Right Click\non background", pos=(250, 150), style=wx.BORDER)
            self.toggle = 0
            self.smoothThread = None


            self.Bind(wx.EVT_BUTTON, self.OnButton)
            self.Bind(wx.EVT_RIGHT_UP, self.OnSmoothThreadMove)
            self.Bind(EVT_UPDATE_SMOOTHMOVE, self.OnUpdate)

        def OnButton(self, event):
            print(event.GetEventObject().GetLabel())

        def OnSmoothThreadMove(self, event=None):
            if self.smoothThread is not None:
                if self.smoothThread.isAlive():
                    print('itsAlive')
                    return
            windoList = [self.ctrl0, self.ctrl1, self.ctrl2]
            if self.toggle:
                moveToPosList = [(50, 50), (250, 350), (450, 50)]
                self.toggle = 0
            else:
                moveToPosList = [(150, 350), (250, 50), (350, 350)]
                self.toggle = 1
            animStepList = [111, 222, 333]
            ctrlCalls = zip(windoList, moveToPosList, animStepList)
            for windo, moveToPos, animStep in ctrlCalls:
                # TODO NOTE: Phoenix is sorta locking up on this one atm...
                # import thread
                # thread.start_new_thread(SmoothMove, (windo, moveToPos, animStep))
                # thread.start_new_thread(self.Run, (windo, moveToPos, animStep))
                # TODO NOTE: Phoenix is locking up on this one atm... but classic isnt.
                stopped = Event()
                self.smoothThread = SmoothThreadMove(stopped, windo, moveToPos, animStep)
                self.smoothThread.start()
            print('OnRightUp')

        def Run(self, windo, moveToPos, animStep):
            if self.smoothThread is not None:
                if self.smoothThread.isAlive():
                    print('itsAlive')
                    return
            windoList = [self.ctrl0, self.ctrl1, self.ctrl2]
            if self.toggle:
                moveToPosList = [(50, 50), (250, 350), (450, 50)]
                self.toggle = 0
            else:
                moveToPosList = [(150, 350), (250, 50), (350, 350)]
                self.toggle = 1
            animStepList = [111, 222, 333]
            ctrlCalls = zip(windoList, moveToPosList, animStepList)
            for windo, moveToPos, animStep in ctrlCalls:
                # We communicate with the UI by sending events to it. There can be
                # no manipulation of UI objects from the worker thread.
                evt = UpdateSmoothMoveEvent(windo=windo, moveToPos=moveToPos, animStep=animStep)
                wx.PostEvent(self, evt)
        def OnUpdate(self, evt):
            SmoothMove(evt.windo, evt.moveToPos, evt.animStep)

    class AnimationTestFrame(wx.Frame):
        """"""
        def __init__(self, parent, id=wx.ID_ANY, title=wx.EmptyString,
                     pos=wx.DefaultPosition, size=wx.DefaultSize,
                     style=wx.DEFAULT_FRAME_STYLE, name='frame'):
            """"""
            wx.Frame.__init__(self, parent, id, title, pos, size, style, name)
            wxVER = 'wxPython %s' % wx.version()
            pyVER = 'python %d.%d.%d.%s' % sys.version_info[0:4]
            versionInfos = '%s %s' % (wxVER, pyVER)
            self.CreateStatusBar().SetStatusText(versionInfos)

            nb = wx.Notebook(self, -1)
            panel1 = AnimationTestPanel1(nb)
            panel2 = AnimationTestPanel2(nb)
            panel3 = AnimationTestPanel3(nb)
            nb.AddPage(panel1, 'SmoothMove')
            nb.AddPage(panel2, 'SmoothMultiMove')
            nb.AddPage(panel3, 'SmoothThreadMove')
            szr = wx.BoxSizer()
            szr.Add(nb, 1, wx.EXPAND)
            self.SetSizerAndFit(szr)

            self.Bind(wx.EVT_CLOSE, self.OnDestroy)

        def OnDestroy(self, event):
            self.Destroy()

    class AnimationTestApp(wx.App):
        def OnInit(self):
            gMainWin = AnimationTestFrame(None)
            gMainWin.SetSize((600, 500))
            gMainWin.SetTitle('Animation Test Frame')
            self.SetTopWindow(gMainWin)
            gMainWin.Center()
            gMainWin.Show()
            return True


    gApp = AnimationTestApp(redirect=False,
            filename=None,
            useBestVisual=False,
            clearSigInt=True)
    gApp.MainLoop()
