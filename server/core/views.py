

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