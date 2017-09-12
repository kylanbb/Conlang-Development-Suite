
"""A lexicon manager/dictionary. Different views, filterable, editable."""

from sys import path
import os.path
if path[0] == os.path.dirname(__file__):
    # modify sys.path so that it points to src, not to src/dictionary
    path[0] = os.path.dirname(path[0]) # parent directory

import common
import wx

class DictionaryWin(common.CDSWin):
    title = "CDS Dictionary"
    _selected = 0
    def __init__(self):
        super().__init__()
        # substitute Dictionary with implementation class here:
        self.dict = Dictionary()
    
    def build(self):
        from dictionary import filtering
        
        self.frame.Sizer = wx.BoxSizer(wx.VERTICAL)
        
        # on top, the filter panel
        self.dictFilter = filtering.Filter(self)
        self.frame.Sizer.Add(self.dictFilter.panel, proportion=0, flag=wx.EXPAND)
        self.dictFilter.build()
        # below, the entry list and entry properties
        # in a SplitterWindow so the width can be adjusted
        self.splitter = wx.SplitterWindow(self.frame, style=wx.SP_LIVE_UPDATE)
        self.frame.Sizer.Add(self.splitter, proportion=1, flag=wx.EXPAND)
        
        self.bottom = wx.Panel(self.frame)
        self.frame.Sizer.Add(self.bottom, proportion=0, flag=wx.EXPAND)
        self.bottom.Sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        self.addButton = wx.Button(self.bottom, id=wx.ID_ADD)
        self.removeButton = wx.Button(self.bottom, id=wx.ID_REMOVE)
        self.bottom.Sizer.Add(self.addButton, proportion=1, flag=wx.ALL, border=5)
        self.bottom.Sizer.Add(self.removeButton, proportion=1, flag=wx.ALL, border=5)
        
        # entries in a ListBox to the left, properties on the right get their own class
        self.entriesBox = wx.ListBox(self.splitter, style=wx.LB_NEEDED_SB|wx.LB_SORT)
        self.entryProperties = EntryProperties(self)
        self.splitter.SplitVertically(self.entriesBox, self.entryProperties.panel, sashPosition=150)
        
        self.bottom.Bind(wx.EVT_BUTTON, lambda e: self.newEntry(), self.addButton)
        self.bottom.Bind(wx.EVT_BUTTON, lambda e: self.removeEntry(), self.removeButton)
        self.frame.Bind(wx.EVT_LISTBOX_DCLICK, self.onEntryDoubleClick, self.entriesBox)
        
    
    def filter(self, filterOptions):
        # use the filterOptions to filter the entry list on the left
        # this requires keeping all the entries in a data structure and building the
        # list box contents dynamically
        # either: filteredEntries = self.dict.filter(filterOptions)
        # then clear the list box and populate with the filtered entries (easy to code)
        # or (harder to code, but faster): iterate over the list box’s items and remove
        # those that don’t satisfy the filter.
        pass
        
    def newEntry(self, entry=None):
        if entry is None: entry = Entry()
        # add entry to the dictionary data structure
        # keeping its unique key (index or whatever)
        key = self.dict.add(entry)
        # add the word to the list box and store the key as cliënt data
        self.entriesBox.Append(entry.word, key)
    
    def removeEntry(self, index=None):
        if index is None: index = self._selected
        # remove it from the dictionary backend
        removed = self.dict.delete(self.entriesBox.GetClientData(index))
        # remove it from the ListBox
        self.entriesBox.Delete(index)
    
    def onEntryDoubleClick(self, event):
        if self.entryProperties.modified and not self.entryProperties.askSave():
            self.entriesBox.Selection = self._selected # restore selection
            return
        self._selected = event.Selection;
        key = event.ClientData
        self.entryProperties.load(self.dict.getEntry(key))

class EntryProperties:
    "The entry properties pane on the right"
    def __init__(self, parent):
        self.parent = parent
        self.panel = wx.Panel(parent.splitter)
    def build(self):
        "Build the GUI and everything belonging to it."
        # text entries for all the entry properties, like word, POS,
        # pronunciation, translation/meaning, usage notes, derivation links
        pass

class Dictionary:
    "Abstract class for the data structure storing the dictionary."
    def get(self, key):
        pass
    def add(self, entry):
        return 0
    def delete(self, key):
        return Entry()
    def filter(self, filterOptions):
        # return a mapping from key to item
        return {}

class Entry:
    "Data class for everything associated with a dictionary entry"
    def __init__(self, word=""):
        self.word = word
        ...

