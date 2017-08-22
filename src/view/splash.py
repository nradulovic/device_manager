'''
Created on Jul 18, 2017

@author: nenad
'''

from gi.repository import Gtk


class Splash(Gtk.Window):
    def __init__(self):
        super(Splash, self).__init__()
        self.props.default_width = 600
        self.props.default_height = 200
        self.props.resizable = False
        self.set_position(Gtk.WindowPosition.CENTER)
        grid = Gtk.Grid()
        grid.props.column_homogeneous = False
        grid.props.row_homogeneous = False
        self.label = Gtk.Label()
        self.label.props.hexpand = True
        self.label.props.vexpand = True
        self.spinner = Gtk.Spinner()
        self.spinner.props.vexpand = True
        grid.attach(self.label, 1, 1, 1, 1)
        grid.attach(self.spinner, 1, 2, 1, 1)
        self.add(grid)

    def set_title(self, title):
        self.props.title = title
        self.spinner.start()

    def set_text(self, text):
        self.label.set_text(text)
