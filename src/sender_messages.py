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

    async def send_msg(self, custom_msg: dict = None, type_msg: Message = None):
        msg: bytes = bytes()
        if custom_msg:
            msg: bytes = json.dumps(custom_msg).encode()
        if type_msg:
            msg: bytes = type_msg.value.encode()

        await self.split_data(msg)

    async def read_msg(self):
        msg = (await self.reader.read(1536)).decode()
        return msg

    async def __aenter__(self):
        self.reader, self.writer = await asyncio.open_connection('192.168.50.223', 8082, ssl=ssl_manager.context)

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        self.writer.close()
        await self.writer.wait_closed()
        if exc_val:
            raise

    async def split_data(self, data: bytes) -> bytes:
        for chunk in (data[_:_+0xffff] for _ in range(0, len(data), 0xffff)):
            self.writer.write(len(chunk).to_bytes(2, "big"))
            await self.writer.drain()
            self.writer.write(chunk)
            await self.writer.drain()
        self.writer.write(b'\x00\x00')
        await self.writer.drain()