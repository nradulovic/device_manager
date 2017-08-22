'''
Created on Jul 4, 2017

@author: nenad
'''
import json
import os

import lib


DEFAULT_CONFIGURATION_PATH = 'res/config'

class ConfigLoader(lib.app_object.AppObject):
    CONFIG_EXT = '.json'

    def __init__(self, path):
        super().__init__()
        self.__path = path
        self.__domains = {}
        files = [x for x in os.listdir(path) \
                 if os.path.isfile(os.path.join(path, x))]
        self.config_files = []
        for file in files:
            if file.endswith(ConfigLoader.CONFIG_EXT):
                self.config_files.append(file)
        self.logger.info('found {} configuration files'.
                format(len(self.config_files)))

    def load(self):
        for file in self.config_files:
            with open(os.path.join(self.__path, file)) as json_file:
                try:
                    keys = json.load(json_file)
                except ValueError as e:
                    self.logger.error(
                            'Failed to load \'{}\' configuration file: {}'
                            .format(file, e.args[0]))
                    # Continue to next file
                    continue
            domain = file.strip(ConfigLoader.CONFIG_EXT)
            self.__domains.update({domain: keys})
            self.logger.info('loaded \'{}\' configuration'.format(domain))
        return self

    def get(self, domain, key_path, default_value=None):
        # Convert to list if argument is plain string
        if isinstance(key_path, str):
            key_path = [key_path]
        key = None
        try:
            keys = self.__domains[domain]
        except KeyError:
            self.logger.warn('Failed to access domain: \'{}\''.format(domain))
            return default_value
        try:
            for key_name in key_path:
                if key is None:
                    key = keys[key_name]
                else:
                    key = key[key_name]
        except KeyError as e:
            self.logger.warn('Failed to fetch key: {} in \'{}\''.
                    format(e, '/'.join([domain] + key_path)))
            return default_value
        else:
            return key


instance = ConfigLoader(DEFAULT_CONFIGURATION_PATH).load()
