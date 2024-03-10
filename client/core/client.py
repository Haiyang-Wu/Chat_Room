"""
core logic

"""

import socket
from conf.settings import *


class MySocket:
    def __init__(self, host='localhost', port=9000):
        self.host = host
        self.port = port
        self.user = None
        self.token = None
        self.online_users = tuple()
        self.socket = None


    def send(self, data):
        self.socket.send(data)

    def recv(self, recv_len):
        return self.socket.recv(recv_len)

    def connect(self):
        for i in range(1,4):
            try:
                self.socket = socket.socket()
                self.socket.connect((self.host, self.port))
                LOGGER.debug('connected to server successfully!')
                return True
            except Exception as e:
                ERROR_LOGGER.error('fail to connect to server, reconnect times:{}! {}'.format(i, e))
                self.socket.close()

    def __enter__(self):
        if self.connerct():
            return self
        else:
            exit()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.socket.close()
def run():
    # connect server
    with MySocket(HOST, PORT)as client:
        # show interface of log in
