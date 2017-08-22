'''
Created on Jul 27, 2017

@author: nenad
'''

import view


class TableModelColumn(object):
    def __init__(self, item):
        self.name = item[0]
        self.handle = item[1]['handle']
        self.id_num = item[1]['id']


class TableModelData(object):
    def __init__(self, dict_data_set, table_model):
        self.dict_data_set = dict_data_set
        self.table_model = table_model
        self.table_data = []
        for name in self.table_model.column_names:
            try:
                self.table_data += [self.dict_data_set[name]]
            except KeyError:
                self.table_data += ['N/A']

    def on_selected(self):
        print(self.table_data)


class TableModelStore(object):
    '''
    This class manages data sets for table views.
    '''
    def __init__(self, dict_table_config):
        '''
        Constructor
        '''
        self.table_config = dict_table_config
        self.column_names = []
        self.column_handles = []
        self.data_sets = {}
        self.data_id_num = 0
        for id_num in range(len(self.table_config)):
            self.column_names += [self.find_column_by_id(id_num).name]
            self.column_handles += [self.find_column_by_id(id_num).handle]
        self.store = view.Gtk.ListStore(*[str] * len(self.table_config))

    def find_column_by_id(self, id_num):
        for item in self.table_config.items():
            if id_num == item[1]['id']:
                return TableModelColumn(item)
        raise IndexError('No such column with \'{}\' ID number'.format(id_num))

    def find_column_by_name(self, name):
        for item in self.table_config.items():
            if name == item[0]:
                return TableModelColumn(item)
        raise IndexError('No such column with \'{}\' name'.format(name))

    def find_column_by_handle(self, handle):
        for item in self.table_config.items():
            if handle == item[1]['handle']:
                return TableModelColumn(item)
        raise IndexError('No such column with \'{}\' handle'.format(handle))

    def add_data(self, dict_table_data):
        table_model_data = TableModelData(dict_table_data, self)
        tree_iter = self.store.append(table_model_data.table_data)
        tree_iter_string = self.store.get_string_from_iter(tree_iter)
        self.data_sets[tree_iter_string] = table_model_data
        return table_model_data

    def on_selection(self, selection):
        model, treeiter = selection.get_selected()
        tree_iter_string = model.get_string_from_iter(treeiter)
        table_model_data = self.data_sets[tree_iter_string]
        table_model_data.on_selected()
