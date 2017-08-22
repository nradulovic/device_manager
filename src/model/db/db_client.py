'''
Created on Jul 27, 2017

@author: nenad
'''
import abc

from lib import app_object


class DBClient(app_object.AppObject, metaclass=abc.ABCMeta):
    @property
    @abc.abstractclassmethod
    def ip_address(self):
        return '127.0.0.1'

    @property
    @abc.abstractclassmethod
    def status(self):
        return 'idle'

    @property
    @abc.abstractclassmethod
    def message(self):
        return 'no message'

    # WARNING: Do not override this method
    @ip_address.setter
    def ip_address(self, ip):
        raise AttributeError('It\'s forbidden to set ip_address attribute')

    @abc.abstractmethod
    def connect(self):
        pass

    @abc.abstractmethod
    def disconnect(self):
        pass
