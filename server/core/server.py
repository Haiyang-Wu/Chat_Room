"""
Core logic

"""

import asyncio

from lib.common import *

class ChatServer:
    def __init__(self, host='localhost', port=9000):
        self.host = host
        self.port = port

        asyncio.run(self.run_server())
    async def client_handler(self, reader, writer):
        async with Myconn(reader, writer)as conn:
            while True:
                request_dic = await conn.recv()
    async def run_server(self):
        server = await asyncio.start_server(self.client_handler, self.host, self.port)
        async with server:
            await server.serve_forever()


    asyncio.run(run_server())