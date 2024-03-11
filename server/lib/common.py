"""
public method
"""
import asyncio
import pickle
import hashlib
from datetime import datetime
from multiprocessing import Queue
from conf.settings import *


# generate token
def generate_token(user):
    hash_obj = hashlib.sha256()
    hash_obj.update(user.encode('utf-8'))
    hash_obj.update(str(datetime.now().date()).encode('utf-8'))
    hash_obj.update('CHATROOM'.encode('utf-8'))
    return hash_obj.hexdigest()

class ResponseData:
    notice = NOTICE

    @staticmethod
    def register_success_dic(msg, *args, **kwargs):
        """
        Organization registration successful dictionary

        :param msg:
        :param args:
        :param kwargs:
        :return:
        """
        response_dic = {
            'code': RESPONSE_SUCCESS_CODE,
            'mode': RESPONSE_REGISTER,
            'msg': msg
        }
        return response_dic

    @staticmethod
    def register_error_dic(msg, *args, **kwargs):
        """
               register error dictionary
               :param msg:
               :param args:
               :param kwargs:
               :return:
               """
        response_dic = {
            'code': RESPONSE_ERROR_CODE,
            'mode': RESPONSE_REGISTER,
            'msg': msg
        }
        return response_dic

    @staticmethod
    def login_success_dic(user, token, msg, *args, **kwargs):
        """
        login successful dictionary
        :param token:
        :param user:
        :param msg:
        :param args:
        :param kwargs:
        :return:
        """
        response_dic = {
            'code': RESPONSE_SUCCESS_CODE,
            'mode': RESPONSE_LOGIN,
            'user': user,
            'msg': msg,
            'token': token,
            'notice': ResponseData.notice,
            'users': tuple(MyConn.online_users.keys())
        }
        return response_dic

    @staticmethod
    def login_error_dic(user, msg, *args, **kwargs):
        """
        login error dictionary
        :param user:
        :param msg:
        :param args:
        :param kwargs:
        :return:
        """
        response_dic = {
            'code': RESPONSE_ERROR_CODE,
            'mode': RESPONSE_LOGIN,
            'user': user,
            'msg': msg
        }
        return response_dic

    @staticmethod
    def online_dic(user, *args, **kwargs):
        """
        online broadcast dictionary
        :param user:
        :param args:
        :param kwargs:
        :return:
        """
        response_dic = {
            'code': RESPONSE_SUCCESS_CODE,
            'mode': RESPONSE_BROADCAST,
            'status': RESPONSE_ONLINE,
            'user': user,
        }
        return response_dic

    @staticmethod
    def offline_dic(user, *args, **kwargs):
        """
        offline broadcast dictionary
        :param user:
        :param args:
        :param kwargs:
        :return:
        """
        response_dic = {
            'code': RESPONSE_SUCCESS_CODE,
            'mode': RESPONSE_BROADCAST,
            'status': RESPONSE_OFFLINE,
            'user': user,
        }
        return response_dic

class MyConn:
    online_users = {}
    bcst_q = Queue()

    def __init__(self, reader, writer):
        self.reader = reader
        self.writer = writer

        self.name = None
        self.token = None  # to judge if a user is a legal user

    async def put_q(self, dic):
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(None, self.bcst_q.put, dic)


    @classmethod
    async def send_all(cls):
        loop = asyncio.get_running_loop()
        while True:
            dic = await loop.run_in_executor(None, cls.bcst_q.get)
            for conn in cls.online_users.values():
                if conn.name == dic.get('user'):
                    continue
                await conn.send(dic)

    async def write(self, data):
        self.writer.write(data)
        await self.writer.drain()

    async def send(self, dic):
        dic_bytes = pickle.dumps(dic)
        len_bytes = len(dic_bytes).to_bytes(PROTOCOL_LENGTH, byteorder='big')
        await self.write(len_bytes)
        await self.write(dic_bytes)
        LOGGER.debug('发送字典完成')
        if dic.get('mode') != RESPONSE_FILE:
            return

        # send file

    async def read(self, recv_len):
        return await self.reader.read(recv_len)

    async def recv(self):
        len_bytes = await self.read(PROTOCOL_LENGTH)
        if not len_bytes:
            raise ConnectionResetError
        stream_len = int.from_bytes(len_bytes, byteorder='big')
        dic_bytes = bytes()
        while stream_len > 0:
            if stream_len < 4096:
                temp = await self.read(stream_len)
            else:
                temp = await self.read(4096)
            if not temp:
                raise ConnectionResetError
            dic_bytes += temp
            stream_len -= len(temp)
        request_dic = pickle.loads(dic_bytes)
        return request_dic

        # receive data of file

    async def offline(self):
        self.online_users.pop(self.name)
        LOGGER.info('[{}] have left the chat room'.format(self.name))
        response_dic = ResponseData.offline_dic(self.name)
        await self.put_q(response_dic)



    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        self.writer.close()
        if self.name:
            await self.offline()
        if exc_type is ConnectionResetError:
            return True
        if (exc_type is not None) and LEVEL != 'DEBUG':
            ERROR_LOGGER.error('{}: {} {}'.format(
                exc_type.__name__, exc_val, exc_tb.tb_frame
            ))
            return True
