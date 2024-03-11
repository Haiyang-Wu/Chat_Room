

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
