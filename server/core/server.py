"""
Core logic

"""

from server.lib.common import *
from server.core.function.urls import route_mode
import ssl


class ChatServer:
    def __init__(self, host='localhost', port=9000):
        self.host = host
        self.port = port
        KEY_FILE = "server-key.pem"
        CERT_FILE = "server-cert.pem"
        self.context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        self.context.load_cert_chain(certfile=CERT_FILE, keyfile=KEY_FILE)
        # context.load_verify_locations(CA_FILE)
        self.context.verify_mode = ssl.CERT_NONE

        # asyncio.run(asyncio.wait([self.run_server(), MyConn.send_all()]))

    async def client_handler(self, reader, writer):
        async with MyConn(reader, writer)as conn:
            while True:
                request_dic = await conn.recv() # get dictionary from client
                # request_dic.get('mode') means the dictionary of function
                # fn is the specific function functions which is a Coroutine Function
                fn = route_mode.get(request_dic.get('mode'))
                await fn(conn, request_dic)
    async def run_server(self):
        ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        KEY_FILE = "server-key.pem"
        CERT_FILE = "server-cert.pem"
        ssl_context.load_cert_chain(certfile=CERT_FILE, keyfile=KEY_FILE)

        server = await asyncio.start_server(self.client_handler, self.host, self.port, ssl=self.context)
        async with server:
            LOGGER.debug('Server started successfully {}'.format((self.host, self.port)))
            await server.serve_forever()

    async def start(self):
        # 此方法将启动所有必要的任务
        server_task = asyncio.create_task(self.run_server())
        send_all_task = asyncio.create_task(MyConn.send_all())
        await asyncio.wait([server_task, send_all_task])

# def run():
#     ChatServer(HOST, PORT)

def run():
    chat_server = ChatServer(HOST, PORT)
    asyncio.run(chat_server.start())