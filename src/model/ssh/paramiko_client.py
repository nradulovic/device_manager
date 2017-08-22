'''
Created on Aug 22, 2017

@author: nenad
'''

from model.ssh import ssh_client
import paramiko
from paramiko import ssh_exception as pexc


class Paramiko(ssh_client.SSHClient):

    def __init__(self, ip_address, username, password, allow_unsafe=True):
        super().__init__(ip_address, username, password)
        self.ssh = paramiko.SSHClient()
        if allow_unsafe:
            self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    def connect(self):
        try:
            self.ssh.connect(self.ip_address, self.username, self.password)
        except (
                pexc.BadHostKeyException,
                pexc.AuthenticationException,
                pexc.SSHException) as e:
            raise RuntimeError('Failed to connect {}'.format(e.args))

    def execute(self, command):
        '''Execute the command.

        Args:
            * command (:obj:`str`): String to execute as a command

        Example::

            ssh.execute('sudo uptime')
            ssh.exec_input('password\n')
            print(ssh.exec_output())
        '''
        self.streams = self.ssh.exec_command(command)

    def exec_input(self, user_input):
        '''Enter user_input for current execution

        Args:
            * command (:obj:`str`): String to input to command
        '''
        stdin, _, _ = self.streams
        stdin.write(user_input)
        stdin.flush()

    def exec_output(self):
        _, stdout, _ = self.streams
        return stdout.read.splitlines()
