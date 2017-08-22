'''
Created on Aug 22, 2017

@author: nenad
'''


class SSHClient(object):

    def __init__(self, ip_address, username, password):
        self.ip_address = ip_address
        self.username = username
        self.password = password

    def connect(self):
        pass
