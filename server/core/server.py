from server.lib.common import *
from server.core.function.urls import route_mode
import ssl
import asyncio

class ChatServer:
    def __init__(self, host='localhost', port=9000):
        """
        Initializes the chat server with SSL context for secure connections.
        """
        self.host = host
        self.port = port
        KEY_FILE = "server-key.pem"
        CERT_FILE = "server-cert.pem"
        self.context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        self.context.load_cert_chain(certfile=CERT_FILE, keyfile=KEY_FILE)
        self.context.verify_mode = ssl.CERT_NONE  # Adjust as necessary for client verification

    async def client_handler(self, reader, writer):
        """
        Handles client connections and requests.
        """
        async with MyConn(reader, writer) as conn:
            while True:
                request_dic = await conn.recv()  # Receive request dictionary from client
                fn = route_mode.get(request_dic.get('mode'))  # Retrieve the corresponding function
                if fn:
                    await fn(conn, request_dic)  # Execute the function

    async def run_server(self):
        """
        Starts the SSL secured server.
        """
        server = await asyncio.start_server(self.client_handler, self.host, self.port, ssl=self.context)
        async with server:
            LOGGER.debug(f'Server started successfully at {self.host}:{self.port}')
            await server.serve_forever()

    async def start(self):
        """
        Launches the server and additional necessary tasks.
        """
        server_task = asyncio.create_task(self.run_server())
        send_all_task = asyncio.create_task(MyConn.send_all())  # Assuming MyConn.send_all is a coroutine
        await asyncio.wait([server_task, send_all_task])

def run():
    """
    Entry point for running the chat server.
    """
    chat_server = ChatServer(HOST, PORT)
    asyncio.run(chat_server.start())
