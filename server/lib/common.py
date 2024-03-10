"""
public method
"""
import pickle

from conf.settings import *


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
            'users': ('小飞', '中飞', '大飞')
        }
        return response_dic


class MyConn:
    def __init__(self, reader, writer):
        self.reader = reader
        self.writer = writer

        self.name = None
        self.token = None  # to judge if a user is a legal user


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



    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        self.writer.close()
        if exc_type is ConnectionResetError:
            return True
        if (exc_type is not None) and LEVEL != 'DEBUG':
            ERROR_LOGGER.error('{}: {} {}'.format(
                exc_type.__name__, exc_val, exc_tb.tb_frame
            ))
            return True
