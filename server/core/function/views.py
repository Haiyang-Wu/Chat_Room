from server.db.connection import connect_to_database
from server.lib.common import *  # Debugging logs
from server.core.function.tools import *

"""
User Registration
"""


async def register(conn, request_dic, *args, **kwargs):
    """
    Registration Interface
    :param conn:
    :param request_dic:
    :param args:
    :param kwargs:
    :return:
    """
    LOGGER.debug('Start register')  # Start registration log
    # Verify if username exists
    user = request_dic.get('user')
    pwd = request_dic.get('pwd')

    # Check if username already exists
    connection = await connect_to_database()
    async with connection.cursor() as cursor:
        await cursor.execute("SELECT * FROM users WHERE username=%s", (user,))
        existing_user = await cursor.fetchone()

    # Handle existing username
    if existing_user:
        response_dic = ResponseData.register_error_dic(f'Account [{user}] already exists, please try again')
        await conn.send(response_dic)
        return

    # Add new user to database
    async with connection.cursor() as cursor:
        await cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (user, pwd))
        await connection.commit()

    # Cleanup resources and return success message
    response_dic = ResponseData.register_success_dic('Registered successfully')
    await conn.send(response_dic)
    await connection.close()


"""
User Login
"""


async def login(conn, request_dic, *args, **kwargs):
    LOGGER.debug('Start login')  # Log start of login
    user = request_dic.get('user')  # Get username from request
    pwd = request_dic.get('pwd')  # Get password from request

    # Establish database connection
    async with await connect_to_database() as connection:  # Assuming this is a context-managed connection
        async with connection.cursor() as cursor:
            await cursor.execute("SELECT password FROM users WHERE username=%s", (user,))
            user_record = await cursor.fetchone()

    if not user_record or user_record[0] != pwd:
        # If user does not exist or password does not match
        response_dic = ResponseData.login_error_dic(user, 'username or password error')
        await conn.send(response_dic)
        await connection.close()  # Close database connection
        return

    if user in conn.online_users:
        # Check if user is already logged in
        response_dic = ResponseData.login_error_dic(user, 'Please dont login the same user!')
        await conn.send(response_dic)
        await connection.close()  # Close database connection
        return

    # Save current conn object
    conn.online_users[user] = conn
    conn.name = user
    conn.token = generate_token(user)  # Assuming there is a function for generating token
    LOGGER.info(f'[{user}] have entered the chat room')  # Log user login info
    response_dic = ResponseData.login_success_dic(user, conn.token, 'login successfully')
    await conn.send(response_dic)

    # Broadcast message
    response_dic = ResponseData.online_dic(user)
    await conn.put_q(response_dic)  # Assuming there is a function for handling message queues


async def reconnect(conn, request_dic, *args, **kwargs):
    """
    Reconnect Interface
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

    # Save current conn object
    conn.online_users[user] = conn
    conn.name = user
    conn.token = token
    LOGGER.info(f'[{user}] have entered the chat room')
    response_dic = ResponseData.reconnect_success_dic()
    await conn.send(response_dic)

    # Broadcast message
    response_dic = ResponseData.online_dic(user)
    await conn.put_q(response_dic)


async def chat(conn, request_dic, *args, **kwargs):
    """
    Chat Interface
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

    # Generate a unique message id
    message_id = generate_unique_message_id()
    # Store message to database
    await store_message_to_database(user, msg, message_id)
    LOGGER.info(f'{user} says: {msg}')
    # Modify chat_dic function to include message ID
    response_dic = ResponseData.chat_dic(message_id, request_dic)
    await conn.put_q(response_dic)


"""
Message Revocation
"""


async def revoke_message_if_possible(message_id, user_id):
    async with await connect_to_database() as conn:
        async with conn.cursor() as cur:
            # Verify if the message exists, belongs to the user requesting revocation, and is within the revocation time window
            await cur.execute(
                "SELECT timestamp FROM messages WHERE message_id=%s AND user_id=%s AND status='sent'",
                (message_id, user_id,)
            )
            result = await cur.fetchone()
            if result:
                # Simplify processing here, assume all messages can be revoked, actual application should check the timestamp
                await cur.execute(
                    "UPDATE messages SET status='revoked' WHERE id=%s",
                    (message_id,)
                )
                await conn.commit()
                return True, "Message revoked"
            else:
                return False, "Message cannot be revoked"


async def file(conn, request_dic, *args, **kwargs):
    """
    Files Interface
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
    # Assume file content is transmitted in binary form
    file_size = request_dic.get('file_size')

    # Save file to server's filesystem
    save_path = request_dic.get('file_path')  # Modify path according to actual situation
    # with open(save_path, "wb") as file:
    #     file.write(file_content)

    # Record file information to database
    file_id = await save_file_info_to_database(user, file_name, file_size, save_path)

    LOGGER.info(f'{user} sent files: {file_name}')
    response_dic = ResponseData.file_dic(file_id, request_dic)
    await conn.put_q(response_dic)
