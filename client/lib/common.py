"""
public method

"""

import hashlib
from datetime import datetime, timezone
from PyQt6.QtWidgets import QMessageBox
from client.conf.settings import *


# Hash encryption
def hash_pwd(pwd):
    hash_obj = hashlib.sha256()
    hash_obj.update('vx'.encode('utf-8'))
    hash_obj.update(pwd.encode('utf-8'))
    hash_obj.update('c3036539'.encode('utf-8'))
    return hash_obj.hexdigest()

def get_time():
    return datetime.now().replace(microsecond=0)

def get_file_info(file_path):
    file_name = os.path.basename(file_path)
    hash_obj = hashlib.md5()
    with open(file_path, 'rb')as f:
        f.seek(0, 2)
        file_size = f.tell()
        one_tenth = file_size // 10
        for i in range(10):
            f.seek(i * one_tenth, 0)
            res = f.read(100)
            hash_obj.update(res)
        return file_name, file_size, hash_obj.hexdigest()


# Reconnection decoration
def reconnect(fn):
    def wrapper(*args, **kwargs):
        self = args[0]
        try:
            res = fn(*args, **kwargs)
        except Exception as e:
            LOGGER.error('Connection down, reconnecting {}'.format(e))
            self.tip_label.setText('Connection down, reconnecting...')
            self.tip_label.setFixedSize(self.tip_label.size())
            self.tip_label.adjustSize()
            self.tip_label.show()
            self.client.close()
            res = self.client.connect()
            self.tip_label.close()
            if res:
                return
            QMessageBox.warning(self,'hint', 'Fail to connect to server, program will be terminated')
            exit()
        return res
    return wrapper


def reconnect_t(fn):
    def wrapper(*args, **kwargs):
        self = args[0]
        try:
            res = fn(*args, **kwargs)
        except Exception as e:
            LOGGER.error('Connection down, reconnecting {}'.format(e))
            # signal
            self.reconnected.emit('show_tip')


            self.client.close()
            res = self.client.connect()

            # signal
            self.reconnected.emit('close_tip')
            if res:
                return
            # signal
            self.reconnected.emit('over')
            self.terminate()

        return res
    return wrapper


def byte_to_human(size):
    units = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
    for unit in units:
        if size < 1024 or unit == 'PB':
            return '{:.2f} {}'.format(size, unit)
        size /= 1024

class RequestData:
    @staticmethod
    def register_dic(user, pwd, *args, **kwargs):
        """
        register dictionary
        :param user:
        :param pwd:
        :param args:
        :param kwargs:
        :return:
        """
        request_dic = {
            'mode': REQUEST_REGISTER,
            'user': user,
            'pwd': hash_pwd(pwd)
        }
        return request_dic

    @staticmethod
    def login_dic(user, pwd, *args, **kwargs):
        """
        Login dictionary
        :param user:
        :param pwd:
        :param args:
        :param kwargs:
        :return:
        """
        request_dic = {
            'mode': REQUEST_LOGIN,
            'user': user,
            'pwd': hash_pwd(pwd)
        }
        return request_dic

    @staticmethod
    def chat_dic(user, msg, token, *args, **kwargs):
        """
        chat dictionary
        :param user:
        :param msg:
        :param token:
        :param args:
        :param kwargs:
        :return:
        """
        request_dic = {
            'mode': REQUEST_CHAT,
            'user': user,
            'msg': msg,
            'time': get_time(),
            'token': token
        }
        return request_dic

    @staticmethod
    def file_dic(user, file_path, token, *args, **kwargs):
        """
        file dictionary
        :param user:
        :param file_path:
        :param token:
        :param args:
        :param kwargs:
        :return:
        """
        file_name, file_size, file_md5 = get_file_info(file_path)
        request_dic = {
            'mode': REQUEST_FILE,
            'user': user,
            'file_name': file_name,
            'file_size': file_size,
            'md5': file_md5,
            'time': get_time(),
            'token': token,
            'file_path': file_path
        }
        return request_dic

    @staticmethod
    def reconnect_dic(user, token, *args, **kwargs):
        """
        组织重连字典
        :param user:
        :param token:
        :param args:
        :param kwargs:
        :return:
        """
        request_dic = {
            'mode': REQUEST_RECONNECT,
            'user': user,
            'token': token
        }
        return request_dic