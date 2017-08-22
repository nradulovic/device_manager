'''
Created on Jul 18, 2017

@author: nenad
'''

import view


class AppException(Exception):
    def __init__(self, msg, text, parent_win=None):
        super(AppException, self).__init__()

        if parent_win is not None:
            def notify_gui_handler():
                notify = view.notification.Notify(
                        parent_win,
                        view.notification.NotifyType.ERR,
                        view.notification.NotifyButton.CLOSE,
                        msg,
                        text)
                notify.show()
                view.Gtk.main_quit()
            view.GLib.idle_add(notify_gui_handler)
