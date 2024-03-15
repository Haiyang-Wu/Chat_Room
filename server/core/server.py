"""
Core logic

"""

from server.lib.common import *
from server.core.function.urls import route_mode


class ChatServer:
    def __init__(self, host='localhost', port=9000):
        self.host = host
        self.port = port

        asyncio.run(asyncio.wait([self.run_server(), MyConn.send_all()]))

    async def client_handler(self, reader, writer):
        async with MyConn(reader, writer)as conn:
            while True:
                request_dic = await conn.recv()
                fn = route_mode.get(request_dic.get('mode'))
                await fn(conn, request_dic)
    async def run_server(self):
        server = await asyncio.start_server(self.client_handler, self.host, self.port)
        async with server:
            LOGGER.debug('Server started successfully {}'.format((self.host, self.port)))
            await server.serve_forever()


def run():
    ChatServer(HOST, PORT)

