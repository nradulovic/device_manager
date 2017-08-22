'''
Created on Jul 18, 2017

@author: nenad
'''
# Standard library imports
import sys

from pyeds import __version__ as pyeds_version
from pyeds import fsm
import lib
import model
import view


class MainFSM(fsm.StateMachine):
    logger = lib.logging.default

    def on_exception(self, exc, exc_state, exc_event, msg):
        self.logger.exception(
                'Exception in \'{}\' occurred at \'{}\' on event \'{}\''
                .format(self.name, exc_state.name, exc_event.name))
        event = fsm.Event('exception')
        event.exc = exc
        event.exc_state = exc_state
        event.exc_event = exc_event
        self.send(event)


@fsm.DeclareState(MainFSM)
class Initalization(fsm.State):
    def on_init(self):
        return Booting


@fsm.DeclareState(MainFSM)
class Operating(fsm.State):

    def on_init(self):
        return Booting

    def on_terminate(self, event):
        return Terminated

    def on_exception(self, event):
        self.sm.rm.register(event)
        return ExceptionState

    def on_view_delete(self, event):
        return Terminated


@fsm.DeclareState(MainFSM)
class Terminated(fsm.State):
    def on_entry(self):
        view.sm.send(fsm.Event('terminate'))
        self.sm.do_terminate()


@fsm.DeclareState(MainFSM)
class ExceptionState(fsm.State):
    def on_entry(self):
        view.sm.send(self.sm.rm.pop('exception'))

    def on_done_exception(self, event):
        return Terminated


@fsm.DeclareState(MainFSM)
class Booting(fsm.State):
    super_state = Operating

    def on_entry(self):
        view.sm.send(fsm.Event('splash'))

    def on_exit(self):
        view.sm.send(fsm.Event('purge'))

    def on_init(self):
        return BootingStage1


@fsm.DeclareState(MainFSM)
class BootingStage1(fsm.State):
    super_state = Booting

    def on_entry(self):
        event = fsm.Event('show_splash')
        event.title = 'Device manager'
        event.text = 'Loading configuration...'
        view.sm.send(event)
        fsm.After(0.3, 'done_stage1')

    def on_done_stage1(self, event):
        return BootingStage2


@fsm.DeclareState(MainFSM)
class BootingStage2(fsm.State):
    super_state = Booting

    def on_entry(self):
        event = fsm.Event('set_text')
        event.text = 'Validating configuration...'
        view.sm.send(event)
        fsm.After(0.3, 'done_stage2')

    def on_done_stage2(self, event):
        return BootingStage3


@fsm.DeclareState(MainFSM)
class BootingStage3(fsm.State):
    super_state = Booting

    def on_entry(self):
        event = fsm.Event('set_text')
        event.text = 'Checking server connection...'
        view.sm.send(event)
        fsm.After(0.3, 'done_stage3')

    def on_done_stage3(self, event):
        return MainWorkloadState


@fsm.DeclareState(MainFSM)
class MainWorkloadState(fsm.State):
    super_state = Operating

    def on_entry(self):
        view.sm.send(fsm.Event('main'))

    def on_exit(self):
        view.sm.send(fsm.Event('purge'))

    def on_init(self):
        return ActivateServer


@fsm.DeclareState(MainFSM)
class ActivateServer(fsm.State):
    super_state = MainWorkloadState

    def on_entry(self):
        event = fsm.Event('set_status')
        event.text = 'Connecting to server ({})...'.format(
                model.db.instance.ip_address)
        view.sm.send(event)
        model.db.instance.connect()
        fsm.After(1.0, 'check_connection')

    def on_check_connection(self, event):
        if model.db.instance.status == 'fatal':
            raise Exception('Failed to connect to server: {}'.format(
                    model.db.instance.message))
        elif model.db.instance.status == 'connecting':
            event = fsm.Event('set_status')
            event.text = 'Waiting for connection...'
            view.sm.send(event)
            return ActivateServerWait
        elif model.db.instance.status == 'connected':
            event = fsm.Event('set_status')
            event.text = 'Connected'
            view.sm.send(event)

    def on_retry_connect(self, event):
        return ActivateServer


@fsm.DeclareState(MainFSM)
class ActivateServerWait(fsm.State):
    super_state = MainWorkloadState

    def on_entry(self):
        fsm.After(1.0, 'wait_done')

    def on_wait_done(self, event):
        return ActivateServer


if __name__ == '__main__':
    lib.logging.setup_additional('device_manager', 'debug')
    lib.logging.default.info('Using PyEDS version {}'.format(pyeds_version))
    sm = MainFSM()
    sys.exit(view.main.looper())
