import asyncio
import json
from enum import Enum

from request_type import RequestType
from ssl_manager import ssl_manager


class Message(str, Enum):
    PING = 'p'
    CONNECTION = 'c'


class SenderMsg:

    def __init__(self):
        self.reader: asyncio.StreamReader | None = None
        self.writer: asyncio.StreamWriter | None = None

    async def send_msg(self, custom_msg: dict):
        msg: bytes = json.dumps(custom_msg).encode()

        self.writer.write(msg)
        await self.writer.drain()

    async def read_msg(self):
        msg = (await self.reader.read(1536)).decode()
        return msg

    async def __aenter__(self):
        self.reader, self.writer = await asyncio.open_connection('10.0.0.183', 8082, ssl=ssl_manager.context)

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        self.writer.close()
        await self.writer.wait_closed()
        if exc_val:
            raise

    @staticmethod
    async def send_error(function: str, e_msg: any):
        error_sender = SenderMsg()
        request = {
            'type': RequestType.ERROR.value,
            'error_info': {
                'function': function,
                'msg': e_msg
            }
        }
        async with error_sender:
            await error_sender.send_msg(request)
