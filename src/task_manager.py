import json
import os

import aiofiles
import aiofiles.os
import asyncio
from src.handlers.host_discovery_handler import HostDiscoveryHandler
from src.write_manager import WriteManager
from src.sender_messages import SenderMsg
from request_type import RequestType
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
    async def write_task(data: dict, run_after_writing: bool):
        id_task = data.get('task_id')
        name_file = os.sep.join([os.getcwd(), 'tasks', f'{id_task}.json'])

        async with aiofiles.open(name_file, mode='w+') as write_handle:
            await write_handle.write(json.dumps(data))

        if run_after_writing:
            execute_task = asyncio.create_task(TaskManager.run_task(id_task, data, False))
            await execute_task
            # TaskManager.execute_tasks.add(execute_task)
            # execute_task.add_done_callback(TaskManager.execute_tasks.discard)

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
                await WriteManager.write_result(task_id, result)

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
            await SenderMsg.send_error('send_result', e.args)

    # @staticmethod
    # async def check_queue():
    #     task_type = task.get('task_type')
    #     match task_type:
    #         case 0:
    #     await asyncio.create_task(TaskManager.run_task(TaskManager.tasks.pop()))
