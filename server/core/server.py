"""
Core logic
"""

from server.lib.common import *
from server.core.function.urls import route_mode


class ChatServer:
    def __init__(self, host='localhost', port=9000):
        self.host = host
        self.port = port
        # asyncio.run(asyncio.wait([self.run_server(), MyConn.send_all()]))

    async def client_handler(self, reader, writer):
        async with MyConn(reader, writer) as conn:
            while True:
                request_dic = await conn.recv()  # Get dictionary from client
                # request_dic.get('mode') returns the dictionary of function
                # fn is the specific function functions which is a Coroutine Function
                fn = route_mode.get(request_dic.get('mode'))
                if fn is not None:
                    await fn(conn, request_dic)

    async def run_server(self):
        server = await asyncio.start_server(self.client_handler, self.host, self.port)
        async with server:
            LOGGER.debug(f'Server started successfully {(self.host, self.port)}')
            await server.serve_forever()

    async def start(self):
        # This method will start all necessary tasks
        server_task = asyncio.create_task(self.run_server())
        send_all_task = asyncio.create_task(MyConn.send_all())
        await asyncio.wait([server_task, send_all_task])


def run():
    chat_server = ChatServer(HOST, PORT)
    asyncio.run(chat_server.start())

# if __name__ == "__main__":
#     run()
