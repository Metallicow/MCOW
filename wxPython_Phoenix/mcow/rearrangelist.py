#!/usr/bin/env python
# -*- coding: utf-8 -*-

# -------------------------------------------------------------------------- #
# REARRANGELIST wxPython IMPLEMENTATION
#
# (c) Edward Greig, @ 25 Sep 2015 - RearrangeList
# Latest Revision: Edward Greig @ 25 Sep 2015, 21.00 GMT
#
# TODO List
#
# 0. Any ideas?
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
# -------------------------------------------------------------------------- #

"""
wx.lib.mcow.rearrangelist.py
============================

This widget is implemented in Phoenix but not Classic(At least not as of this writing).
...so reimplement it for wxPython Classic.

`RearrangeList` is a listbox-like control allowing the user to rearrange the
items and to enable or disable them.


Usage
-----

Usage example::

    import wx
    import wx.lib.mcow.rearrangelist as RAL

    class MyFrame(wx.Frame):
        def __init__(self, parent):
            wx.Frame.__init__(self, parent, -1, "RearrangeList Demo")

            ral = RAL.RearrangeList(self, order=[0, 1, 0, 1, 1],
                                    items=['One', 'Two', 'Three', 'Four', 'Five'])
            vbSizer = wx.BoxSizer(wx.VERTICAL)
            vbSizer.Add(ral, 1, wx.EXPAND | wx.ALL, 5)
            self.SetSizer(vbSizer)

    # our normal wxApp-derived class, as usual

    app = wx.App(0)

    frame = MyFrame(None)
    app.SetTopWindow(frame)
    frame.Show()

    app.MainLoop()


Methods and Settings
--------------------

With `RearrangeList` you can:

- CanMoveCurrentDown();
- CanMoveCurrentUp();
- GetCurrentOrder();
- MoveCurrentDown();
- MoveCurrentUp();


Supported Platforms
-------------------
:class:`RearrangeList` has been tested on the following platforms:
  * Windows (Windows 7).


License And Version
-------------------

`RearrangeList` is distributed under the wxPython license.

Edward Greig, @ 25 Sep 2015
Latest revision: Edward Greig @ 25 Sep 2015, 21.00 GMT

Version 0.1

"""

import wx

class RearrangeList(wx.CheckListBox):
    """
    **Possible constructors**::

        RearrangeList()

        RearrangeList(parent, id=ID_ANY, pos=DefaultPosition, size=DefaultSize,
                      order=[], items=[], style=0, validator=DefaultValidator,
                      name=RearrangeListNameStr)

    A listbox-like control allowing the user to rearrange the items and to
    enable or disable them.
    """
    def __init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition,
                 size=wx.DefaultSize, order=[], items=[], style=0,
                 validator=wx.DefaultValidator, name='RearrangeListNameStr'):
        wx.CheckListBox.__init__(self, parent, id, pos, size, [], style, validator, name)
        """
        |overload| **Overloaded Implementations**:

        **~~~**

        **__init__** `(self)`

        Default constructor.

        :meth:`Create`   must be called later to effectively create the control.

        **~~~**

        **__init__** `(self, parent, id=ID_ANY, pos=DefaultPosition, size=DefaultSize, order=[], items=[], style=0, validator=DefaultValidator, name=RearrangeListNameStr)`

        Constructor really creating the control.

        Please see :meth:`Create`   for the parameters description.

        :param `parent`:
        :type `parent`: Window
        :param `id`:
        :type `id`: int
        :param `pos`:
        :type `pos`: Point
        :param `size`:
        :type `size`: Size
        :param `order`:
        :type `order`: list of integers
        :param `items`:
        :type `items`: list of strings
        :param `style`:
        :type `style`: long
        :param `validator`:
        :type `validator`: Validator
        :param `name`:
        :type `name`: string

        **~~~**
        """
        self.order = order
        self.items = items

        if items:
            self_Insert = self.Insert
            self_Check = self.Check
            for i, item in enumerate(items):
                if order[i] >= 0:
                   self_Insert(items[order[i]], i)
                else:
                   self_Insert(items[abs(order[i] + 1)], i)
                self_Check(i, check=order[i] >= 0)

        self.Bind(wx.EVT_CHECKLISTBOX, self.UpdateOrder)


    def UpdateOrder(self, event):
        event.Skip()
        index = event.GetInt()
        order = self.order.pop(index)
        if order >= 0:
            self.order.insert(index, -order - 1)
        else:
            self.order.insert(index, abs(order + 1))
        ## print('self.order = %s' % self.order)

    def CanMoveCurrentDown(self):
        """
        Return ``True`` if the currently selected item can be moved down.

        :rtype: `bool`

        .. seealso:: :meth:`CanMoveCurrentUp`
        """
        selection = self.GetSelection()
        if selection == -1:  # No selected listitem
            return False
        else:
            if len(self.items) > 1:  # Need more than 1 item to move
                if selection + 1 != len(self.items):
                    return True
            return False

    def CanMoveCurrentUp(self):
        """
        Return ``True`` if the currently selected item can be moved up.

        This function is useful for ``EVT_UPDATE_UI`` handler for the standard
        "Up" button often used together with this control and :ref:`RearrangeCtrl`
        uses it in this way.

        :returns: ``True`` if the currently selected item can be moved up in the listbox,
         ``False`` if there is no selection or the current item is the first one.
        :rtype: `bool`

        .. seealso:: :meth:`CanMoveCurrentDown`
        """
        selection = self.GetSelection()
        if selection == -1:  # No selected listitem
            return False
        else:
            if len(self.items) > 1:  # Need more than 1 item to move
                if selection:  # Greater than zero
                    return True
            return False

    def Create(self, parent, id, pos, size, order, items, style, validator, name):
        """
        Effectively creates the window for an object created using the default constructor.

        This function is very similar to :meth:`CheckListBox.Create` except that
        it has an additional parameter specifying the initial order of the items.
        Please see the class documentation for the explanation of the conventions
        used by the `order` argument.

        :param `parent`: The parent window, must be not ``None``.
        :type `parent`: Window
        :param `id`: The window identifier.
        :type `id`: int
        :param `pos`: The initial window position.
        :type `pos`: Point
        :param `size`: The initial window size.
        :type `size`: Size
        :param `order`: Array specifying the initial order of the items in  `items`  array.
        :type `order`: list of integers
        :param `items`: The items to display in the list.
        :type `items`: list of strings
        :param `style`: The control style, there are no special styles for this class but the base class styles can be used here.
        :type `style`: long
        :param `validator`: Optional window validator.
        :type `validator`: Validator
        :param `name`: Optional window name.
        :type `name`: string

        :rtype: `bool`
        """
        raise NotImplementedError

    @property
    def CurrentOrder(self):
        return self.order

    def GetCurrentOrder(self):
        """
        Return the current order of the items.

        The order may be different from the one passed to the constructor if
        :meth:`MoveCurrentUp` or :meth:`MoveCurrentDown` were called.

        :rtype: `list of integers`
        """
        return self.order

    def MoveCurrentDown(self):
        """
        Move the currently selected item one position below.

        :rtype: `bool`

        .. seealso:: :meth:`MoveCurrentUp`
        """
        if self.CanMoveCurrentDown():
            index = self.GetSelection()
            order = self.order.pop(index)
            self.order.insert(index + 1, order)
            self.Delete(index)
            if order >= 0:
               self.Insert(self.items[self.order[index + 1]], index + 1)
            else:
               self.Insert(self.items[abs(self.order[index + 1] + 1)], index + 1)
            self.Check(index + 1, check=order >= 0)
            self.SetSelection(index + 1)
            return True
        else:
            return False

    def MoveCurrentUp(self):
        """
        Move the currently selected item one position above.

        This method is useful to implement the standard "Up" button behaviour
        and :ref:`RearrangeCtrl` uses it for this.

        :returns: ``True`` if the item was moved or ``False`` if this couldn't be done.
        :rtype: `bool`

        .. seealso:: :meth:`MoveCurrentDown`
        """
        if self.CanMoveCurrentUp():
            index = self.GetSelection()
            order = self.order.pop(index)
            self.order.insert(index - 1, order)
            self.Delete(index)
            if order >= 0:
               self.Insert(self.items[self.order[index - 1]], index - 1)
            else:
               self.Insert(self.items[abs(self.order[index - 1] + 1)], index - 1)
            self.Check(index - 1, check=order >= 0)
            self.SetSelection(index - 1)
            return True
        else:
            return False


class RearrangeCtrl(wx.Panel):
    """
    A composite control containing a RearrangeList and the buttons
    allowing to move the items in it.
    """
    def __init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition,
                 size=wx.DefaultSize, order=[], items=[], style=0,
                 validator=wx.DefaultValidator, name='RearrangeListNameStr'):
        """
        |overload| **Overloaded Implementations**:

        **~~~**

        **__init__** `(self)`

        Default constructor.

        :meth:`Create` must be called later to effectively create the control.

        **~~~**

        **__init__** `(self, parent, id=ID_ANY, pos=DefaultPosition, size=DefaultSize, order=[], items=[], style=0, validator=DefaultValidator, name=RearrangeListNameStr)`

        Constructor really creating the control.

        Please see :meth:`Create` for the parameters description.

        :param `parent`:
        :type `parent`: Window
        :param `id`:
        :type `id`: int
        :param `pos`:
        :type `pos`: Point
        :param `size`:
        :type `size`: Size
        :param `order`:
        :type `order`: list of integers
        :param `items`:
        :type `items`: list of strings
        :param `style`:
        :type `style`: long
        :param `validator`:
        :type `validator`: Validator
        :param `name`:
        :type `name`: string

        **~~~**
        """
        wx.Panel.__init__(self, parent, id, pos, size, style, name)

        self.rearrangelist = ral = RearrangeList(self,
                                                 order=order,
                                                 items=items)
        self.btnup = btnup = wx.Button(self, -1, 'Up')
        btnup.Bind(wx.EVT_BUTTON, self.OnMoveCurrentUp)
        btnup.Enable(False)
        self.btndown = btndown = wx.Button(self, -1, 'Down')
        btndown.Bind(wx.EVT_BUTTON, self.OnMoveCurrentDown)
        btndown.Enable(False)
        hbSizer = wx.BoxSizer(wx.HORIZONTAL)
        hbSizer.Add(ral, 1, wx.EXPAND | wx.ALL, 0)
        vbSizer = wx.BoxSizer(wx.VERTICAL)
        vbSizer.AddStretchSpacer()
        vbSizer.Add(btnup, 0, wx.EXPAND | wx.ALL, 5)
        vbSizer.Add(btndown, 0, wx.EXPAND | wx.ALL, 5)
        vbSizer.AddStretchSpacer()
        hbSizer.Add(vbSizer, 0, wx.EXPAND | wx.ALL, 0)
        ral.Bind(wx.EVT_LISTBOX, self.OnListBox)
        ral.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        ral.Bind(wx.EVT_MOTION, self.OnMotion)
        self.SetSizer(hbSizer)

    def OnListBox(self, event):
        event.Skip()
        self.EnableButtons()

    def OnLeftDown(self, event):
        event.Skip()
        wx.CallAfter(self.EnableButtons)

    def OnMotion(self, event):
        event.Skip()
        if event.Dragging and event.LeftIsDown:
            self.EnableButtons()

    def EnableButtons(self):
        self.btnup.Enable(self.rearrangelist.CanMoveCurrentUp())
        self.btndown.Enable(self.rearrangelist.CanMoveCurrentDown())

    def OnMoveCurrentDown(self, event):
        self.rearrangelist.MoveCurrentDown()
        wx.CallAfter(self.EnableButtons)

    def OnMoveCurrentUp(self, event):
        self.rearrangelist.MoveCurrentUp()
        wx.CallAfter(self.EnableButtons)

    @property
    def List(self):
        return self.rearrangelist

    def GetList(self):
        """
        Return the listbox which is the main part of this control.

        :rtype: :ref:`RearrangeList`
        """
        return self.rearrangelist


if __name__ == '__main__':
    # Sample App.
    class MyFrame(wx.Frame):
        def __init__(self, parent):
            wx.Frame.__init__(self, parent, -1, "RearrangeList RearrangeCtrl Demo")

            self.rac = rac = RearrangeCtrl(self,
                                           # order=[0, 1, 2, -4, 4, 5],
                                           # order=[5, -5, 3, 2, 1, -1],
                                           order=[5, -5, -4, -3, 1, -1],
                                           items=['Zero', 'One', 'Two', 'Three', 'Four', 'Five'])
            btncurorder = wx.Button(self, -1, 'GetCurrentOrder')
            btncurorder.Bind(wx.EVT_BUTTON, self.OnGetCurrentOrder)
            vbSizer = wx.BoxSizer(wx.VERTICAL)
            vbSizer.Add(rac, 1, wx.EXPAND | wx.ALL, 5)
            vbSizer.Add(btncurorder, 0, wx.EXPAND | wx.ALL, 5)
            self.SetSizer(vbSizer)

        def OnGetCurrentOrder(self, event):
            event.Skip()
            print(self.rac.List.CurrentOrder)
            print(self.rac.GetList().GetCurrentOrder())
            print('OnGetCurrentOrder')

    # our normal wxApp-derived class, as usual

    app = wx.App(0)

    frame = MyFrame(None)
    app.SetTopWindow(frame)
    frame.Show()

    app.MainLoop()