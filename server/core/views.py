

from db.models import User
from lib.common import *
async def register(conn, request_dic, *args, **kwargs):
    """
    Registration Interface
    :param conn:
    :param request_dic:
    :param args:
    :param kwargs:
    :return:
    """
    LOGGER.debug('Start register')
    user = request_dic.get('user')
    pwd = request_dic.get('pwd')
    if await User.select(user):
        response_dic = ResponseData.register_error_dic('Account [{}] already exists, please try again'.format(user))
        await conn.send(response_dic)
        return
    user_obj = User(user, pwd)
    await user_obj.save()
    response_dic = ResponseData.register_success_dic('Registered successfully')
    await conn.send(response_dic)


async def login(conn, request_dic, *args, **kwargs):
    """
    login Interface
    :param conn:
    :param request_dic:
    :param args:
    :param kwargs:
    :return:
    """
    LOGGER.debug('Start login')
    user = request_dic.get('user')
    pwd = request_dic.get('pwd')
    user_obj = await User.select(user)
    if not user_obj or user_obj.pwd != pwd:
        response_dic = ResponseData.login_error_dic(user, 'username or password error')
        await conn.send(response_dic)
        return

    if user in conn.online_users:
        response_dic = ResponseData.login_error_dic(user, 'Please dont login the same user!')
        await conn.send(response_dic)
        return

    # save current conn object
    conn.online_users[user] = conn
    conn.name = user
    conn.token = generate_token(user)
    LOGGER.info('[{}] have entered the chat room'.format(user))
    response_dic = ResponseData.login_success_dic(user, conn.token, 'login successfully')
    await conn.send(response_dic)

    # broadcast message
    response_dic = ResponseData.online_dic(user)
    await conn.put_q(response_dic)

async def reconnect(conn, request_dic, *args, **kwargs):
    """
    reconnect Interface
    :param conn:
    :param request_dic:
    :param args:
    :param kwargs:
    :return:
    """
    LOGGER.debug('start reconnect')
    token = request_dic.get('token')
    user = request_dic.get('user')
    if generate_token(user) != token:
        response_dic = ResponseData.reconnect_error_dic('token is invalid, please try again')
        await conn.send(response_dic)
        return

    if user in conn.online_users:
        response_dic = ResponseData.reconnect_error_dic('user already login')
        await conn.send(response_dic)
        return

    # save current conn object
    conn.online_users[user] = conn
    conn.name = user
    conn.token = token
    LOGGER.info('[{}] have entered the chat room'.format(user))
    response_dic = ResponseData.reconnect_success_dic()
    await conn.send(response_dic)

    # broadcast message
    response_dic = ResponseData.online_dic(user)
    await conn.put_q(response_dic)


async def chat(conn, request_dic, *args, **kwargs):
    """
    chat interface
    :param conn:
    :param request_dic:
    :param args:
    :param kwargs:
    :return:
    """
    token = request_dic.get('token')
    if token != conn.token:
        conn.close()
        return
    user = request_dic.get('user')
    msg = request_dic.get('msg')
    LOGGER.info('{} says: {}'.format(user, msg))
    response_dic = ResponseData.chat_dic((request_dic))
    await conn.put_q(response_dic)


async def file(conn, request_dic, *args, **kwargs):
    """
    files interface
    :param conn:
    :param request_dic:
    :param args:
    :param kwargs:
    :return:
    """
    token = request_dic.get('token')
    if token != conn.token:
        conn.close()
        return

    user = request_dic.get('user')
    file_name = request_dic.get('file_name')
    LOGGER.info('{} sended files: {}'.format(user, file_name))
    response_dic = ResponseData.file_dic((request_dic))
    await conn.put_q(response_dic)


