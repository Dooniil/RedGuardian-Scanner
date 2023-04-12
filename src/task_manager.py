import json
import os
import threading
import aiofiles
import asyncio
from src.executors.HD import HostDiscovery


class TaskManager:
    queue = asyncio.Queue()
    request_path = os.sep.join([os.getcwd(), 'temp', 'requests'])
    tasks = []

    @staticmethod
    async def fill_queue():
        for file in os.listdir(os.path.join(TaskManager.request_path)):
            if os.path.isfile(os.path.join(TaskManager.request_path, file)):
                async with aiofiles.open(os.path.join(TaskManager.request_path, file), mode='r') as handle:
                    data = await handle.read()
                    task = asyncio.create_task(TaskManager.run_task(json.loads(data)))
                    await TaskManager.queue.put(task)

    @staticmethod
    async def write_req_to_tmp(data: dict):
        id_task = data.get("task_id")
        name_file = os.sep.join([os.getcwd(), 'temp', 'requests', f'{id_task}.json'])

        async with aiofiles.open(name_file, mode='w') as handle:
            await handle.write(json.dumps(data))

        await TaskManager.fill_queue()

    @staticmethod
    async def write_res_to_tmp(task_id, result: list):
        name_file = os.sep.join([os.getcwd(), 'temp', 'result', f'{task_id}.json'])

        async with aiofiles.open(name_file, mode='w') as handle:
            for item in result:
                await handle.write(json.dumps(item))

    @staticmethod
    async def run_task(task_info: dict):
        task_type = task_info.get('type_task')
        match task_type:
            case 0:
                hd_setting = task_info.get('settings')
                host_discovery = HostDiscovery()
                th = threading.Thread(target=host_discovery.scan, args=(
                    hd_setting.get('type'),
                    hd_setting.get('protocols'),
                    hd_setting.get('subnets'),)
                )
                th.start()
                th.join()
                print(host_discovery.result)
                await asyncio.wait([
                    asyncio.create_task(TaskManager.write_res_to_tmp(task_info.get('task_id'),
                                                                     host_discovery.result))])

    @staticmethod
    async def check_queue():
        while not TaskManager.queue.empty():
            TaskManager.tasks.append(TaskManager.queue.get())

        if TaskManager.tasks:
            await asyncio.gather(*TaskManager.tasks)

        await asyncio.sleep(10)
