import asyncio
import json
from encryption_manager import encryption_manager
#
# HOST = os.environ['HOST']
# PORT = os.environ['PORT']
# CONTROLLER_HOST = os.environ['CONTROLLER_HOST']
# CONTROLLER_PORT = os.environ['CONTROLLER_PORT']
# NAME = os.environ['NAME']


async def read_request(reader) -> str:
    request = bytearray()
    while True:
        request += await reader.read(1536)
        reader.feed_eof()
        if reader.at_eof():
            return request.decode()


async def scanner_handler(reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
    request = await read_request(reader)
    try:
        data = json.loads(request)
        match data.get('type'):
            case 'key':
                encryption_manager.private_key = data.get('key')
                print(encryption_manager.private_key)
                writer.write(b'1')
                await writer.drain()
    except json.decoder.JSONDecodeError:
        if request == 'p':
            writer.write('scanner01'.encode())
            await writer.drain()


async def run_server(host) -> None:
    server = await asyncio.start_server(scanner_handler, host, 8084)
    async with server:
        await server.serve_forever()

