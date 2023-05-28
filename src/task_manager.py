import json
import os

import aiofiles
import aiofiles.os
import asyncio
from request_type import RequestType
from src.handlers.host_discovery_handler import HostDiscoveryHandler
from src.handlers.vulnerability_handler import VulnerabilityHandler
from src.sender_messages import SenderMsg
from src.write_manager import WriteManager
from src.time_info_manager import TimeInfoManager


class TaskManager:
    tasks_path = os.sep.join([os.getcwd(), 'tasks'])
    # result_path = os.sep.join([os.getcwd(), 'results'])

    # @staticmethod
    # async def fill_tasks():
    #     for file in os.listdir(os.path.join(TaskManager.tasks_path)):
    #         if os.path.isfile(os.path.join(TaskManager.tasks_path, file)):
    #             async with aiofiles.open(os.path.join(TaskManager.tasks_path, file), mode='r') as handle:
    #                 data = await handle.read()
    #                 task = json.loads(data)
    #                 await TaskManager.tasks.put(task)

    @staticmethod
    async def write_task(data: dict):
        id_task = data.get('task_id')
        name_file = os.sep.join([os.getcwd(), 'tasks', f'{id_task}.json'])

        async with aiofiles.open(name_file, mode='w+') as write_handle:
            await write_handle.write(json.dumps(data))

        return id_task, data

    @staticmethod
    async def run_task(task_id: int, task_data: dict = None, is_need_read: bool = True):
        time_manager = TimeInfoManager()
        time_manager.start()

        if is_need_read:
            async with aiofiles.open(os.path.join(TaskManager.tasks_path, f'{task_id}.json'), mode='r') as read_handle:
                data = await read_handle.read()
                task_data = json.loads(data)

        type_task = task_data.get('type_task')
        result = None
        match type_task:
            case 0:
                result = await asyncio.to_thread(HostDiscoveryHandler.scan, task_data)
            case 1:
                result: dict = await asyncio.to_thread(VulnerabilityHandler.scan, task_data)
                
        write_task = asyncio.create_task(WriteManager.write_result(task_id, result))
        await write_task

        time_manager.stop()
        await TaskManager.send_result(task_id, type_task, result, time_manager.exec_time, time_manager.exec_date)

    @staticmethod
    async def send_result(task_id: int, type_task, result: dict, time, date):
        request = {
            'type': RequestType.RESULT.value,
            'task_id': task_id,
            'type_task': type_task,
            'result_info': result,
            'start_time': date[0],
            'end_time': date[1],
            'exec_time': time
        }
        result_sender = SenderMsg()
        try:
            async with result_sender:
                await result_sender.send_msg(request)
        except Exception as e:
            raise Exception('Error while sending result')
        