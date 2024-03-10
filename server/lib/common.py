"""
public method
"""

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

class Myconn:
    def __init__(self, reader, writer):
        self.reader = reader
        self.writer = writer

        self.name = None
        self.token = None   # to judge if a user is a legal user


    async def read(self, recv_len):
        return await self.reader.read(recv_len)
    async def recv(self):
        dic_len = await self.read(PROTOCOL_LENGTH)

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


