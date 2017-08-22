
import lib
import model

# This is exception to PSG: Use imports for packages and modules only.
from model.db.ftp_client import FTPClient


class DBClientLoader(lib.app_object.AppObject):
    DEFAULT_CLIENT = 'FTPClient'

    def __init__(self):
        super().__init__()
        # Load and instance the class as specified in configuration
        client = model.config.instance.get(
                'core',
                'DBClient',
                DBClientLoader.DEFAULT_CLIENT)
        try:
            self.client = globals()[client]()
        except KeyError:
            self.logger.error('Can\'t find \'{}\' DB client'.format(client))
            self.client = globals()[DBClientLoader.DEFAULT_CLIENT]()
        self.logger.info('loaded \'{}\' client'.format(client))

    def load(self):
        return self.client


instance = DBClientLoader().load()
