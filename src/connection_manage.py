import asyncio
import base64
import json
import socket
from src.encryption_manager import encryption_manager


def conn_to_controller(port) -> None:
    socket_ = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_.bind(('10.0.0.171', port))
    with socket_ as connection:
        connection.connect(('10.0.0.183', 8082))
        connection.send(b'{"cmd":"connecting","name_scanner":"scanner01"}')
        connection.close()


async def scanner_handler(reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
    request = await reader.read(1536)
    data = json.loads(base64.b64decode(request))

    match data.get('type'):
        case 'key':
            encryption_manager.private_key = data.get('key')
            print(encryption_manager.private_key)
            writer.write(b'1')


async def run_server(port: int) -> None:
    server = await asyncio.start_server(scanner_handler, '10.0.0.171', port)
    async with server:
        await server.serve_forever()

