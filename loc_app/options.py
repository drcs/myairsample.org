class TextOptions:

  _selection = []  

  groups = [
    ('both',
     '''an explanation of both units and levels of concern''',
     ['units','levels']),
    ('units',
     '''an explanation of units only''',
     ['units']),
    ('levels',
     '''an explanation of levels of concern only''',
     ['levels']),
    ('none',
     '''no text at the end of the report''',
     []) ]

  def select_group(self, group_name):
      for (name,desc,selection) in self.groups:
          if name == group_name:
              self._selection = selection

  def selected(self, item):
      return item in self._selection

  def selection(self):
      return self._selection

  def group_names(self):
      return map(lambda (k,d,x): (k, d), self.groups)

