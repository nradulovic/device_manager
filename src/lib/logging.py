'''
Created on Jul 5, 2017

@author: nenad
'''
import logging


__formatter = logging.Formatter('%(asctime)s %(levelname)s %(name)s: %(message)s')
__log_levels = {
        'debug' : logging.DEBUG,
        'info' : logging.INFO,
        'warn' : logging.WARN,
        'error' : logging.ERROR
    }

def setup_file_handler(name, level):
    fh = logging.FileHandler('{}.log'.format(name))
    fh.setLevel(__log_levels.get(level, logging.DEBUG))
    fh.setFormatter(__formatter)

    logger = logging.getLogger('app')
    logger.addHandler(fh)

def setup_additional(name, level=None):
    logger = logging.getLogger('app.{}'.format(name))

    if level is not None:
        logger.setLevel(__log_levels.get(level, logging.DEBUG))

    return logger

def __setup_default():
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(__formatter)
    logger = logging.getLogger('app')
    logger.setLevel(logging.DEBUG)
    logger.addHandler(ch)

    return logger

default = __setup_default()
