import json
import os
import aiofiles


class WriteManager:
    result_path = os.sep.join([os.getcwd(), 'results'])

    @staticmethod
    async def write_result(task_id, result):
        name_file = os.path.join(WriteManager.result_path, f'{task_id}.json')
        async with aiofiles.open(name_file, mode='w+') as write_handle:
            await write_handle.write(json.dumps(result))
