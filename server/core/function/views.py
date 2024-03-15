from server.db.connection import connect_to_database
from server.db.models import User
from server.lib.common import *


async def register(conn, request_dic, *args, **kwargs):
    """
    Registration Interface
    :param conn:
    :param request_dic:
    :param args:
    :param kwargs:
    :return:
    """
    LOGGER.debug('Start register')  # 开始注册日志
    # 验证用户名是否存在
    user = request_dic.get('user')
    pwd = request_dic.get('pwd')

    # 检查用户名是否已存在
    connection = await connect_to_database()
    async with connection.cursor() as cursor:
        await cursor.execute("SELECT * FROM users WHERE username=%s", (user,))
        existing_user = await cursor.fetchone()

    # 用户名存在的处理
    if existing_user:
        response_dic = ResponseData.register_error_dic('Account [{}] already exists, please try again'.format(user))
        await conn.send(response_dic)
        return

    # 添加新用户到数据库
    async with connection.cursor() as cursor:
        await cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (user, pwd))
        await connection.commit()

    # 清理资源并返回成功消息
    response_dic = ResponseData.register_success_dic('Registered successfully')
    await conn.send(response_dic)
    await connection.close()


async def login(conn, request_dic, *args, **kwargs):
    LOGGER.debug('Start login')  # 记录登录开始的日志
    user = request_dic.get('user')  # 从请求中获取用户名
    pwd = request_dic.get('pwd')  # 从请求中获取密码

    # 建立数据库连接
    async with await connect_to_database() as connection:  # 假设这里是一个支持上下文管理的连接
        async with connection.cursor() as cursor:
            await cursor.execute("SELECT password FROM users WHERE username=%s", (user,))
            user_record = await cursor.fetchone()

    if not user_record or user_record[0] != pwd:
        # 如果用户不存在或密码不匹配
        response_dic = ResponseData.login_error_dic(user, 'username or password error')
        await conn.send(response_dic)
        await connection.close()  # 关闭数据库连接
        return

    if user in conn.online_users:
        # 检查用户是否已登录
        response_dic = ResponseData.login_error_dic(user, 'Please dont login the same user!')
        await conn.send(response_dic)
        await connection.close()  # 关闭数据库连接
        return

    # 保存当前的conn对象
    conn.online_users[user] = conn
    conn.name = user
    conn.token = generate_token(user)  # 假设存在一个用于生成token的函数
    LOGGER.info('[{}] have entered the chat room'.format(user))  # 记录用户登录的信息日志
    response_dic = ResponseData.login_success_dic(user, conn.token, 'login successfully')
    await conn.send(response_dic)

    # 广播消息
    response_dic = ResponseData.online_dic(user)
    await conn.put_q(response_dic)  # 假设存在一个用于处理消息队列的函数


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
