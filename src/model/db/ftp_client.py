'''
Created on Jul 28, 2017

@author: nenad
'''

import ftplib
import lib
import model
from model.db import db_client
from pyeds import fsm


class FTPClientFSM(fsm.StateMachine):
    logger = lib.logging.default

    def __init__(self, client_data):
        self.client_data = client_data
        self.status = 'initialization'
        self.message = None
        super().__init__()


@fsm.DeclareState(FTPClientFSM)
class Initialization(fsm.State):
    def on_init(self):
        self.sm.ip_address = model.config.instance.get(
                'core',
                'FTP server ip',
                '127.0.0.1')
        self.sm.user = model.config.instance.get(
                'core',
                'FTP server user',
                FTPClient.DEFAULT_USER)
        self.sm.passwd = model.config.instance.get(
                'core',
                'FTP server pass',
                FTPClient.DEFAULT_PASSWD)
        self.logger.info('FTP: server IP is {}'.format(self.sm.ip_address))
        self.logger.info('FTP: using {}:{} credentials'.format(
            self.sm.user, self.sm.passwd))
        return (Idle)


@fsm.DeclareState(FTPClientFSM)
class Idle(fsm.State):
    def on_entry(self):
        self.sm.status = 'idle'

    def on_connect(self, event):
        return Operational


@fsm.DeclareState(FTPClientFSM)
class Operational(fsm.State):
    def on_init(self):
        return Connecting

    def on_fatal_error(self, event):
        return FatalError

    def on_disconnect(self, event):
        return Idle

    def on_reconnect(self, event):
        return Operational


@fsm.DeclareState(FTPClientFSM)
class Connecting(fsm.State):
    super_state = Operational

    def on_init(self):
        self.sm.status = 'connecting'
        self.sm.ftp = ftplib.FTP(self.sm.ip_address)
        try:
            self.sm.ftp.login(self.sm.user, self.sm.passwd)
        except ftplib.error_perm as e:
            self.sm.message = 'permission denied: {}'.format(e.args[0])
            self.logger.error(self.sm.message)
            return FatalError
        else:
            return Connected


@fsm.DeclareState(FTPClientFSM)
class Connected(fsm.State):
    super_state = Operational

    def on_entry(self):
        self.sm.status = 'connected'


@fsm.DeclareState(FTPClientFSM)
class FatalError(fsm.State):
    def on_entry(self):
        self.sm.status = 'fatal'


class FTPClient(db_client.DBClient):
    DEFAULT_USER = 'netico'
    DEFAULT_PASSWD = 'netico'

    def __init__(self):
        super().__init__()
        self.sm = FTPClientFSM(self)

    @property
    def ip_address(self):
        return self.sm.ip_address

    @property
    def status(self):
        return self.sm.status

    @property
    def message(self):
        return self.sm.message

    def connect(self):
        self.sm.send(fsm.Event('connect'))

    def disconnect(self):
        pass
