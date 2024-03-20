"""
public method
"""
import re
import asyncio
import pickle
import hashlib
import aiofiles
from datetime import datetime, timezone
from multiprocessing import Queue
from server.conf.settings import *


# generate token
def generate_token(user):
    hash_obj = hashlib.sha256()
    hash_obj.update(user.encode('utf-8'))
    hash_obj.update(str(datetime.now().date()).encode('utf-8'))
    hash_obj.update('CHATROOM'.encode('utf-8'))
    return hash_obj.hexdigest()


def get_utc_time():
    utc_time = datetime.utcnow().replace(microsecond=0, tzinfo=timezone.utc)
    return utc_time


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

    @staticmethod
    def reconnect_success_dic(*args, **kwargs):
        """
        reconnect success dictionary
        :param args:
        :param kwargs:
        :return:
        """
        response_dic = {
            'code': RESPONSE_SUCCESS_CODE,
            'mode': RESPONSE_RECONNECT,
            'users': tuple(MyConn.online_users.keys())
        }
        return response_dic

    @staticmethod
    def reconnect_error_dic(msg, *args, **kwargs):
        """
        reconnect error dictionary
        :param msg:
        :param args:
        :param kwargs:
        :return:
        """
        response_dic = {
            'code': RESPONSE_ERROR_CODE,
            'mode': RESPONSE_RECONNECT,
            'msg': msg
        }
        return response_dic

    @staticmethod
    def chat_dic(message_id, response_dic, *args, **kwargs):
        """
        chat dictionary
        :param response_dic: The dictionary containing the initial response data.
        :param message_id: The unique identifier for the message.
        :param args: Additional positional arguments (unused here, but for future extensibility).
        :param kwargs: Additional keyword arguments (unused here, but for future extensibility).
        :return: A dictionary representing the chat message response.
        """
        # Remove token, if it exists
        response_dic.pop('token', None)  # Use pop(key, None) to avoid KeyError if the key does not exist
        response_dic['code'] = RESPONSE_SUCCESS_CODE  # Assuming RESPONSE_SUCCESS_CODE is defined
        response_dic['time'] = get_utc_time()  # Assuming get_utc_time() returns the current UTC time

        # If a message_id is provided, add it to the response dictionary
        if message_id is not None:
            response_dic['message_id'] = message_id

        return response_dic

    @staticmethod
    def file_dic(file_id, response_dic, *args, **kwargs):
        """
        Modify the file dictionary to include file ID.

        :param file_id: The unique identifier of the file saved in the database.
        :param response_dic: The original response dictionary.
        :param args: Additional positional arguments.
        :param kwargs: Additional keyword arguments.
        :return: The modified response dictionary with file ID included.
        """
        # Remove token
        response_dic.pop('token', None)  # Use pop(key, None) to avoid KeyError if the key does not exist
        response_dic['code'] = RESPONSE_SUCCESS_CODE  # Assuming RESPONSE_SUCCESS_CODE is defined
        response_dic['time'] = get_utc_time()  # Assuming get_utc_time() returns the current UTC time
        # Add file_id to the response dictionary
        response_dic['file_id'] = file_id

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
            try:
                file_path = dic.pop('file_path')
            except KeyError:
                pass
            for conn in cls.online_users.values():
                if conn.name == dic.get('user'):
                    continue
                await conn.send(dic)
            # send files
            if dic.get('mode') == RESPONSE_FILE:
                await cls.send_file(dic, file_path)

    @classmethod
    async def send_file(cls, dic, file_path):
        async with aiofiles.open(file_path, 'rb')as f:
            while True:
                temp = await f.read(4096)
                if not temp:
                    break
                for conn in cls.online_users.values():
                    if conn.name == dic.get('user'):
                        continue
                    await conn.write(temp)

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
        if request_dic.get('mode') != RESPONSE_FILE:
            return request_dic
        # receive data of file
        return await self.recv_file(request_dic)

    @staticmethod
    def rename(file_name):
        base, ext = os.path.splitext(file_name)
        pattern = re.compile(r'\((d+)\)\$')
        res = pattern.search(base)
        if res:
            num = int(res.group(1)) + 1
            base = pattern.sub('({})'.format(num), base)
        else:
            base = '{}{}'.format(base, '(1)')
        return '{}{}'.format(base, ext)

    async def recv_file(self, request_dic):
        file_size = request_dic.get('file_size')
        now_date = datetime.now().strftime('%Y-%m')
        file_dir = os.path.join(FILE_DIR, now_date)
        if not os.path.isdir(file_dir):
            os.mkdir(file_dir)

        file_name = request_dic.get('file_name')
        file_path = os.path.join(file_dir, file_name)
        while True:
            if os.path.exists(file_path):
                file_name = self.rename(file_name)
                file_path = os.path.join(file_dir, file_name)
            else:
                break
        async with aiofiles.open(file_path, 'wb')as f:
            while file_size > 0:
                if file_size < 4096:
                    temp = await self.read(file_size)
                else:
                    temp = await self.read(4096)
                if not temp:
                    raise ConnectionResetError
                await f.write(temp)
                file_size -= len(temp)
            request_dic['file_path'] = file_path
        return request_dic


    def close(self):
        self.writer.close()

    async def offline(self):
        self.online_users.pop(self.name)
        LOGGER.info('[{}] have left the chat room'.format(self.name))
        response_dic = ResponseData.offline_dic(self.name)
        await self.put_q(response_dic)

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        self.close()
        if self.name:
            await self.offline()
        if exc_type is ConnectionResetError:
            return True
        if (exc_type is not None) and LEVEL != 'DEBUG':
            ERROR_LOGGER.error('{}: {} {}'.format(
                exc_type.__name__, exc_val, exc_tb.tb_frame
            ))
            return True
