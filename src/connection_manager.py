import asyncio
import json
from request_type import RequestType
from src.encryption_manager import encryption_manager
from ssl_manager import ssl_manager
from src.task_manager import TaskManager
from src.sender_messages import SenderMsg
from src.sender_messages import Message


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

            case RequestType.KEY.value:
                try:
                    encryption_manager.private_key = data.get('key')
                    print(encryption_manager.private_key)
                except Exception as e:
                    await SenderMsg.send_error('write_key', e.args)

            case RequestType.SAVE_TASK.value:
                try:
                    await TaskManager.write_task(data.get('task_data'), data.get('run_after_creation'))
                except Exception as e:
                    await SenderMsg.send_error('save_task', e.args)
                    raise Exception(f'Problem while writing to tmp\n{e.args}')

            case RequestType.RUN_TASK.value:
                try:
                    await TaskManager.run_task(data.get('task_id'))
                except Exception as e:
                    await SenderMsg.send_error('run_task', e.args)
                    raise Exception(f'Problem while running\n{e.args}')
    except json.decoder.JSONDecodeError:
        if request == Message.PING.value:
            writer.write('scanner03'.encode())
            await writer.drain()


async def run_server(host) -> None:
    server = await asyncio.start_server(scanner_handler, host, 8084, ssl=ssl_manager.context)
    async with server:
        await server.serve_forever()
