from server.db.connection import connect_to_database
from server.lib.common import *
from server.core.function.tools import *


async def register(conn, request_dic, *args, **kwargs):
    """
    Handles user registration requests. Checks if the user already exists in the database
    and adds a new user if not present.
    """
    LOGGER.debug('Starting registration process')
    user = request_dic.get('user')
    pwd = request_dic.get('pwd')

    # Check if the username already exists
    connection = await connect_to_database()
    async with connection.cursor() as cursor:
        await cursor.execute("SELECT * FROM users WHERE username=%s", (user,))
        existing_user = await cursor.fetchone()

    if existing_user:
        # User already exists
        response_dic = ResponseData.register_error_dic(f'Account [{user}] already exists, please try again.')
        await conn.send(response_dic)
        return

    # Insert new user into database
    async with connection.cursor() as cursor:
        await cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (user, pwd))
        await connection.commit()

    # Send success response
    response_dic = ResponseData.register_success_dic('Registered successfully.')
    await conn.send(response_dic)
    await connection.close()


async def login(conn, request_dic, *args, **kwargs):
    """
    Handles user login requests. Checks username and password against the database
    and processes user login if credentials match.
    """
    LOGGER.debug('Starting login process')
    user = request_dic.get('user')
    pwd = request_dic.get('pwd')

    async with await connect_to_database() as connection:
        async with connection.cursor() as cursor:
            await cursor.execute("SELECT password FROM users WHERE username=%s", (user,))
            user_record = await cursor.fetchone()

    if not user_record or user_record[0] != pwd:
        # Invalid credentials
        response_dic = ResponseData.login_error_dic(user, 'Username or password error.')
        await conn.send(response_dic)
        await connection.close()
        return

    if user in conn.online_users:
        # User already logged in
        response_dic = ResponseData.login_error_dic(user, 'Please don\'t login the same user again!')
        await conn.send(response_dic)
        await connection.close()
        return

    # Successful login
    conn.online_users[user] = conn
    conn.name = user
    conn.token = generate_token(user)  # Assuming a token generation function
    LOGGER.info(f'[{user}] has entered the chat room.')
    response_dic = ResponseData.login_success_dic(user, conn.token, 'Login successfully.')
    await conn.send(response_dic)

    # Broadcast online status
    response_dic = ResponseData.online_dic(user)
    await conn.put_q(response_dic)


async def reconnect(conn, request_dic, *args, **kwargs):
    """
    Handles user reconnection requests, ensuring that the user token is valid
    and that the user is not already connected.
    """
    LOGGER.debug('Starting reconnect process')
    token = request_dic.get('token')
    user = request_dic.get('user')

    if generate_token(user) != token:
        # Invalid token
        response_dic = ResponseData.reconnect_error_dic('Token is invalid, please try again.')
        await conn.send(response_dic)
        return

    if user in conn.online_users:
        # User already online
        response_dic = ResponseData.reconnect_error_dic('User already logged in.')
        await conn.send(response_dic)
        return

    # Successful reconnection
    conn.online_users[user] = conn
    conn.name = user
    conn.token = token
    LOGGER.info(f'[{user}] has re-entered the chat room.')
    response_dic = ResponseData.reconnect_success_dic()
    await conn.send(response_dic)

    # Broadcast online status
    response_dic = ResponseData.online_dic(user)
    await conn.put_q(response_dic)


async def chat(conn, request_dic, *args, **kwargs):
    """
    Handles chat messages from users, storing the messages in the database
    and broadcasting them to other users.
    """
    token = request_dic.get('token')
    if token != conn.token:
        conn.close()
        return
    user = request_dic.get('user')
    msg = request_dic.get('msg')

    # Generate and store message
    message_id = generate_unique_message_id()
    await store_message_to_database(user, msg, message_id)
    LOGGER.info(f'{user} says: {msg}')
    response_dic = ResponseData.chat_dic(message_id, request_dic)
    await conn.put_q(response_dic)


async def file(conn, request_dic, *args, **kwargs):
    """
    Handles file transfer requests from users, saving the files on the server
    and recording the transfer in the database.
    """
    token = request_dic.get('token')
    if token != conn.token:
        conn.close
