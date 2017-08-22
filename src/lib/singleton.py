#!/usr/local/bin/python2.7
# encoding: utf-8

import atexit
import sys
import traceback

from lib import logging


_singletons = []

class Singleton(object):
    _instance = None

    def __init__(self):
        global _singletons

        if self.__class__._instance:
            raise RuntimeError('This class was already instanced!')
        self.__class__._instance = self
        _singletons.append(self)
        super().__init__()

    def __call__(self, *args, **kwargs):
        if hasattr(self, 'on_instance_call'):
            return self.on_instance_call(*args, **kwargs)
        else:
            return self._instance


@atexit.register
def terminate_all_singletons():
    global _singletons

    _singletons.reverse()

    for singleton in _singletons:
        logging.default.info('terminating {0}/{1}'.format(
                singleton.__class__.__module__, singleton.__class__.__name__))

        if hasattr(singleton, 'on_instance_terminate'):
            # NOTE:
            # Swallow all exceptions here. If something fails, just print the
            # information and go on, continue the execution of other terminate
            # methods.
            try:
                singleton.on_instance_terminate()
            except:
                exc_type, exc_value, exc_traceback = sys.exc_info()
                logging.default.error('Unhandled exception: {0} : {1}'.format(
                        exc_type.__name__, exc_value))
                for exc_trace in traceback.extract_tb(exc_traceback, 7)[10:]:
                    logging.default.error('trace: line {0} in {1} at {2}'.format(
                        exc_trace[1], exc_trace[0], exc_trace[2]))

    _singletons = []
