
import lib
import model

# This is exception to PSG: Use imports for packages and modules only.
from model.ssh.paramiko_client import Paramiko


class SSHClientLoader(lib.app_object.AppObject):
    DEFAULT_CLIENT = 'Paramiko'

    def __init__(self):
        super().__init__()
        # Load and instance the class as specified in configuration
        client = model.config.instance.get(
                'core',
                'SSHClient',
                SSHClientLoader.DEFAULT_CLIENT)
        try:
            self.client = globals()[client]()
        except KeyError:
            self.logger.error('Can\'t find \'{}\' SSH client'.format(client))
            self.client = globals()[SSHClientLoader.DEFAULT_CLIENT]()
        self.logger.info('loaded \'{}\' client'.format(client))

    def load(self):
        return self.client


instance = SSHClientLoader().load()
