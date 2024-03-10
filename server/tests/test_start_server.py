import asyncio

async def client_handler(reader, writer):
    while True:
        try:
            data = await reader.read(1024)
            if not data:
                break
            writer.write(data.upper())
            await writer.drain()    # f.flush()
        except ConnectionResetError:
            break
    writer.close()

async def run_server():
    server = await asyncio.start_server(client_handler, 'localhost', 8080)
    async with server:
        await server.serve_forever()


asyncio.run(run_server())