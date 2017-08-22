'''
Created on Jul 6, 2017

@author: nenad
'''
from lib import logging


class AppObject(object):
    # NOTE:
    # This is a kludge. Since some classes are requesting logging before calling
    # to __init__() that actually installs a logging. These classes will
    # therefore print to default logging instead of a customised class logging.
    logging = logging.default

    def __init__(self):
        logger_name = '{0}.{1}'.format(self.__class__.__module__,
                self.__class__.__name__)
        self.logger = logging.setup_additional(logger_name)

        self.logger.debug('initializing {} in {}'.format(
                self.__class__.__name__, self.__class__.__module__))

