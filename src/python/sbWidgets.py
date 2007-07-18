#!/usr/bin/env python
# encoding: utf-8

import wx
import string
from wx.lib.evtmgr import eventManager
        
class CtrlValidator(wx.PyValidator):
    def __init__(self, flag, update_func=None):
        wx.PyValidator.__init__(self)
        self.type = flag
        self.update = update_func
        self.Bind(wx.EVT_CHAR, self.OnChar)
    def Clone(self):
        return CtrlValidator(self.type)        
    def OnChar(self, event):    
        key = event.GetKeyCode()
        val = self.GetWindow().GetValue()
        
        # spaces and escapes and backspaces etc
        if key < wx.WXK_SPACE or key == wx.WXK_DELETE or key > 255:
            event.Skip()
            return
            
        # float
        if self.type=='float':
            if chr(key) in string.digits:
                event.Skip()
                return
            if chr(key)=='.' and not '.' in val:
                event.Skip()
                return
        
        # ring?
        if not wx.Validator_IsSilent():
            wx.Bell()
        return

class Ctrl(wx.Panel):
    def __init__(self, parent, parameter):
        wx.Panel.__init__(self, parent, -1)
        self.parameter = parameter
        self.sizer = wx.BoxSizer( wx.HORIZONTAL )
        self.SetSizer( self.sizer )
        self.lbl = wx.StaticText(self, -1, parameter.getAttribute('name'))
        self.sizer.Add( self.lbl, 0, wx.ALL, 5 )

class FloatCtrl(Ctrl):
    def __init__(self, parent, parameter):
        Ctrl.__init__(self, parent, parameter)
        self.ctrl = wx.TextCtrl(self, -1, validator=CtrlValidator('float', self.update) )        
        self.ctrl.SetValue( parameter.value )
        self.ctrl.Bind( wx.EVT_TEXT, self.update )
        self.sizer.Add( self.ctrl, 1, wx.ALL, 5 )
    def update(self, event):
        self.parameter.setValue(self.ctrl.GetValue())
        event.Skip()
        return

#==============================================================================

# Class for our custom appearance pane
class AppearancePane(wx.Panel):
    def __init__(self, appearance, parent, style):
        wx.Panel.__init__(self, parent, -1, wx.DefaultPosition, wx.DefaultSize, style)
        
        sizer = wx.BoxSizer( wx.VERTICAL )
        self.SetSizer( sizer )

        top_info = wx.Panel( self, -1, style=wx.NO_BORDER)
        top_sizer = wx.BoxSizer( wx.HORIZONTAL )

        preview_img =  wx.BitmapButton( top_info, -1, style = wx.SIMPLE_BORDER, size=(64,64) )      
        top_info_sizer = wx.BoxSizer( wx.VERTICAL )

        top_sizer.Add( preview_img, 0, wx.ALL, 5 )
        top_sizer.Add( top_info_sizer, 0, wx.ALL|wx.EXPAND, 5 )
        top_info.SetSizer( top_sizer )
        sizer.Add( top_info, 0, wx.ALL|wx.EXPAND, 0 )

        for param in appearance.contents:
            widget = self.addParameter( param )
            if widget:
                sizer.Add( widget, 0, wx.ALL, 5 )
    
    def addParameter(self, parameter):
        result = None
        param_type = parameter.getAttribute('type')
        
        if param_type=='colour':
            pass
        elif param_type=='float':
            result = FloatCtrl( self, parameter )
        return result
        
