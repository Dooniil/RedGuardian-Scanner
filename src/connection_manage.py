import asyncio
import json
from src.encryption_manager import encryption_manager
from ssl_manager import ssl_manager
from src.task_manager import TaskManager


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
            case 'run':
                print(data)
                try:
                    await asyncio.wait(asyncio.create_task(TaskManager.write_req_to_tmp(data.get('task_data'))))
                    writer.write(b'1')
                    await writer.drain()
                except:
                    writer.write(b'404')
                    await writer.drain()
                    raise Exception('Problem while writing to tmp')
    except json.decoder.JSONDecodeError:
        if request == 'p':
            writer.write('scanner02'.encode())
            await writer.drain()


async def run_server(host) -> None:
    server = await asyncio.start_server(scanner_handler, host, 8084, ssl=ssl_manager.context)
    async with server:
        await server.serve_forever()
