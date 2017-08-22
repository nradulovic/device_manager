'''
Created on Jul 18, 2017

@author: nenad
'''

from gi.repository import Gtk

from model import config, table


class MainWindow(Gtk.Window):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.set_title(config.instance.get('core', 'app name', 'unknown'))
        self.spacing = config.instance.get('ui', 'spacing')
        self.props.default_width = config.instance.get(
                'ui',
                'default_win_hsize',
                1024)
        self.props.default_height = config.instance.get(
                'ui',
                'default_win_vsize',
                768)
        self.props.resizable = True
        self.set_position(Gtk.WindowPosition.CENTER)
        presentation_grid = Gtk.Grid()
        presentation_grid.props.column_homogeneous = False
        presentation_grid.props.row_homogeneous = False
        presentation_grid.props.column_spacing = self.spacing
        presentation_grid.props.row_spacing = self.spacing
        presentation_grid.props.border_width = self.spacing
        self.action_grid = Gtk.Grid()
        self.action_grid.props.column_spacing = self.spacing
        self.action_grid.props.row_spacing = self.spacing
        self.action_grid.props.border_width = self.spacing
        status_grid = Gtk.Grid()
        status_grid.props.column_spacing = self.spacing
        status_grid.props.row_spacing = self.spacing
        status_grid.props.border_width = self.spacing
        # Create presentation list
        presentation_grid.attach(self.set_table('table'), 0, 0, 8, 10)
        # Create actions
        self.actions = {}
        # Create status
        self.status_bar = Gtk.Label()
        self.status_bar.props.hexpand = True
        self.status_bar.set_xalign(0)
        self.status_bar.set_text('Status: idle')
        status_grid.attach(self.status_bar, 2, 20, 1, 1)
        # Add all grids to window
        box = Gtk.VBox()
        box.pack_start(presentation_grid, True, True, 0)
        box.pack_end(status_grid, False, True, 0)
        box.pack_end(self.action_grid, False, True, 0)
        self.add(box)

    def _on_tree_selection_changed(self, selection):
        self.table_model.on_selection(selection)

    def set_table(self, name):
        self.table_model = table.TableModelStore(
                config.instance.get('ui', name, 'table'))
        self.tree = Gtk.TreeView(self.table_model.store)
        select = self.tree.get_selection()
        select.connect('changed', self._on_tree_selection_changed)
        for i, title in enumerate(self.table_model.column_names):
            renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(title, renderer, text=i)
            self.tree.append_column(column)
        self.scrollable_treelist = Gtk.ScrolledWindow()
        self.scrollable_treelist.set_vexpand(True)
        self.scrollable_treelist.set_hexpand(True)
        self.scrollable_treelist.add(self.tree)
        return self.scrollable_treelist

    def on_action_clicked(self, widget, idx):
        print(idx)

    def add_action(self, name):
        button = Gtk.Button()
        button.props.label = name
        button.props.name = name
        button.props.hexpand = True
        button.props.sensitive = False
        self.actions[name] = button
        self.action_grid.attach(button, len(self.actions) - 1, 0, 1, 1)
        return button

    def add_table_entry(self, data_set):
        return self.table_model.add_data(data_set)
