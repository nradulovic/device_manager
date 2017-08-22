'''
Created on Jul 18, 2017

@author: nenad
'''

from gi.repository import Gtk


class NotifyType(object):
    INFO = Gtk.MessageType.INFO
    WARN = Gtk.MessageType.WARNING
    ERR = Gtk.MessageType.ERROR


class NotifyButton(object):
    OK = Gtk.ButtonsType.OK
    CANCEL = Gtk.ButtonsType.CANCEL
    CLOSE = Gtk.ButtonsType.CLOSE


class Notify(object):
    def __init__(self, parent, message_type, message_button, message, text):
        self.dialog = Gtk.MessageDialog(
                parent,
                0,
                message_type,
                message_button,
                message)
        self.dialog.format_secondary_text(text)

    def show(self):
        self.dialog.run()
        self.dialog.destroy()
