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


async def readexactly(reader, bytes_count: int) -> bytes:
    """
    Функция приёма определённого количества байт
    """
    data_bytes = bytearray()
    while len(data_bytes) < bytes_count: # Пока не получили нужное количество байт
        part = await reader.read(bytes_count - len(data_bytes)) # Получаем оставшиеся байты
        if not part: # Если из сокета ничего не пришло, значит его закрыли с другой стороны
            raise IOError("Соединение потеряно")
        data_bytes += part
    return data_bytes

async def reliable_receive(reader) -> bytes:
    """
    Функция приёма данных
    Обратите внимание, что возвращает тип bytes
    """
    data_bytes = bytearray()
    while True:
        part_len = int.from_bytes(await readexactly(reader, 2), "big") # Определяем длину ожидаемого куска
        if part_len == 0: # Если пришёл кусок нулевой длины, то приём окончен
            return data_bytes
        data_bytes += await readexactly(reader, part_len) # Считываем сам кусок


async def scanner_handler(reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
    request = await reliable_receive(reader)
    try:
        data = json.loads(request)
        match data.get('type'):
            case RequestType.KEY.value:
                try:
                    encryption_manager.private_key = data.get('key')
                    print(encryption_manager.private_key)
                except Exception as e:
                    raise Exception(f'Key receiving problem\n{e.args}')
                    # await SenderMsg.send_error('write_key', e.args)

            case RequestType.SAVE_TASK.value:
                try:
                    run_after_creation = data.get('run_after_creation')
                    id_task, data = await TaskManager.write_task(data.get('task_data'))
                    writer.write(b'0')
                    await writer.drain()
                    if run_after_creation:
                        execute_task = asyncio.create_task(TaskManager.run_task(id_task, data, False))
                        await execute_task
                except Exception as e:
                    # await SenderMsg.send_error('save_task', e.args)
                    raise Exception(f'Problem while writing to tmp\n{e.args}')

            case RequestType.RUN_TASK.value:
                try:
                    await TaskManager.run_task(data.get('task_id'))
                except Exception as e:
                    # await SenderMsg.send_error('run_task', e.args)
                    raise Exception(f'Problem while running\n{e.args}')
    except json.decoder.JSONDecodeError:
        request = bytes(request).decode()
        if request == Message.PING.value:
            writer.write('scanner03'.encode())
            await writer.drain()


async def run_server(host) -> None:
    server = await asyncio.start_server(scanner_handler, host, 8084, ssl=ssl_manager.context)
    async with server:
        await server.serve_forever()
