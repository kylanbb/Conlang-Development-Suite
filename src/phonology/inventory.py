
"""The phoneme inventory editor"""

import wx

from . import main
from . import consonantBank

class InventoryView(main.PhonologyView):
    def build(self):
        # make a split screen with two consonant charts and two vowel trapeziums;
        # one on top for the phonology being edited, one at the bottom for complete IPA
        # … or not
        self.table = ConsonantTable(self, False)
        self.panel.Sizer = wx.BoxSizer(wx.VERTICAL)
        self.panel.Sizer.Add(self.table.panel, 1, flag=wx.EXPAND)
        self.table.build()
        

class ConsonantTable:
    def __init__(self, parent, readOnly):
        self.readOnly = readOnly
        self.panel = wx.Panel(parent.panel)
        self.parent = parent
    
    def build(self):
        # GridBagSizer for all the boxes
        # every phoneme box gets its own window
        # a static text or panel or something? Not sure
        self.panel.Sizer = wx.GridBagSizer(vgap=5, hgap=5)
        
        # not using sets because sets don’t preserve order
        places = []
        manners = []
        # iterate through all the place–manner combinations
        for box in consonantBank.consonants:
            if box.place not in places:
                places.append(box.place)
            if box.manner not in manners:
                manners.append(box.manner)
            ...
            for sound in box.getModels():
                ...
            ...
        
        
        # label the rows and columns
        for col, lbl in enumerate(places, 1):
            self.panel.Sizer.Add(wx.StaticText(self.panel, label=lbl), (0, col), flag=wx.TOP|wx.LEFT|wx.EXPAND, border=5)
            self.panel.Sizer.AddGrowableCol(col, 1)
        for row, lbl in enumerate(manners, 1):
            self.panel.Sizer.Add(wx.StaticText(self.panel, label=lbl), (row, 0), flag=wx.TOP|wx.EXPAND, border=5)
            self.panel.Sizer.AddGrowableRow(row, 1)

