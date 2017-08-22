'''
Created on Jul 18, 2017

@author: nenad
'''

import traceback

from gi.repository import Gtk, GLib, GObject

from pyeds import fsm
import lib

from . import mainwindow
from . import notification
from . import splash


# Since GTK has restrictions when running on multi-threaded model we have to
# use this wrapper to execute the code in the right context.
class RunOnUI(object):
    def __init__(self):
        self.sm = fsm.current()

    def __call__(self, function):
        event = fsm.Event('done_{}'.format(function.__name__))

        def wrapper(sm):
            function(sm)
            sm.send(event)
        GLib.idle_add(wrapper, self.sm)


# View state machine
class ViewFSM(fsm.StateMachine):
    logger = lib.logging.default
    instances = {}

    def __init__(self):
        GObject.threads_init()
        super().__init__()

    def current_window(self):
        return self.win

    def delete_event(self, obj, gdk):
        self.send(fsm.Event('delete'))

    def clicked_event(self, obj):
        event = fsm.Event('clicked')
        event.obj_name = obj.props.name
        self.send(event)


@fsm.DeclareState(ViewFSM)
class Initialization(fsm.State):
    def on_init(self):
        return PurgatoryState


@fsm.DeclareState(ViewFSM)
class Terminate(fsm.State):
    def on_entry(self):
        Gtk.main_quit()
        self.sm.do_terminate()


@fsm.DeclareState(ViewFSM)
class Operating(fsm.State):
    def on_terminate(self, event):
        return Terminate

    def on_exception(self, event):
        @RunOnUI()
        def create_exc_window(sm):
            brief = 'Exception'
            details = ''
            if hasattr(event.exc, 'message'):
                details = 'MESSAGE:\n{}\n\n'.format(event.exc.message)
            details += 'ERROR:\n{}\n\nSOURCE:\n{} {}({})\n\nTRACE:\n{}'.format(
                event.exc,
                event.exc_state.sm.name,
                event.exc_state.name,
                event.exc_event.name,
                '\n'.join(str(item) for item in reversed(
                    traceback.extract_tb(event.exc.__traceback__)[-4:])))
            notify = notification.Notify(
                sm.win,
                notification.NotifyType.ERR,
                notification.NotifyButton.CLOSE,
                brief,
                details)
            notify.show()

    def on_done_create_exc_window(self, event):
        self.sm.client.send(fsm.Event('done_exception'))
        return ExceptionState


@fsm.DeclareState(ViewFSM)
class PurgatoryState(fsm.State):
    super_state = Operating

    def on_entry(self):
        if len(self.sm.instances) > 0:
            @RunOnUI()
            def destroy_instances(sm):
                for instance in sm.instances.values():
                    instance.destroy()

    def on_splash(self, event):
        self.sm.client = event.producer
        return SplashState

    def on_main(self, event):
        self.sm.client = event.producer
        return MainWindowState


@fsm.DeclareState(ViewFSM)
class ActiveState(fsm.State):
    super_state = Operating

    def on_purge(self, event):
        return PurgatoryState


@fsm.DeclareState(ViewFSM)
class SplashState(fsm.State):
    super_state = ActiveState

    def on_entry(self):
        @RunOnUI()
        def create_splash_window(sm):
            sm.win = splash.Splash()
            sm.win.connect('delete-event', self.sm.delete_event)

    def on_exit(self):
        @RunOnUI()
        def destroy_splash_window(sm):
            sm.win.destroy()

    def on_delete(self, event):
        self.sm.client.send(fsm.Event('view_delete'))

    def on_show_splash(self, event):
        @RunOnUI()
        def show_splash_window(sm):
            sm.win.set_title(event.title)
            sm.win.set_text(event.text)
            sm.win.show_all()

    def on_set_text(self, event):
        @RunOnUI()
        def update_text(sm):
            sm.win.set_text(event.text)

    def on_hide_splash(self, event):
        @RunOnUI()
        def hide_splash_window(sm):
            sm.win.hide()


@fsm.DeclareState(ViewFSM)
class MainWindowState(fsm.State):
    super_state = ActiveState

    def on_entry(self):
        @RunOnUI()
        def create_main_window(sm):
            win = mainwindow.MainWindow()
            win.connect('delete-event', self.sm.delete_event)
            win.add_table_entry(
                    {
                        'Name': 'BlueBox Audio',
                    })
            win.add_table_entry(
                    {
                        'Name': 'BlueBox BAD',
                    })
            win.add_action('Add new device').connect(
                    'clicked', self.sm.clicked_event)
            win.add_action('Modify device data').connect(
                    'clicked', self.sm.clicked_event)
            win.show_all()
            sm.win = win

    def on_add_entry(self, event):
        pass

    def on_exit(self):
        @RunOnUI()
        def destroy_main_window(sm):
            sm.win.destroy()

    def on_delete(self, event):
        self.sm.client.send(fsm.Event('view_delete'))

    def on_clicked(self, event):
        if event.obj_name == 'Add new device':
            self.sm.client.send(fsm.Event('v_add_new_device'))

    def on_set_status(self, event):
        @RunOnUI()
        def update_status_bar(sm):
            sm.win.status_bar.set_text('Status: ' + event.text)


@fsm.DeclareState(ViewFSM)
class ExceptionState(fsm.State):
    super_state = ActiveState


def looper():
    return Gtk.main()


view_fsm = ViewFSM()
