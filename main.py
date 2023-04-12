from src.connection_manage import run_server
import asyncio
from src.task_manager import TaskManager
from address import choose_host


async def main():
    host = '192.168.50.223' # choose_host()
    tasks = [
        asyncio.create_task(run_server(host)),
        asyncio.create_task(TaskManager.check_queue()),
    ]
    await asyncio.wait([asyncio.create_task(TaskManager.fill_queue())])
    await asyncio.gather(*tasks)
    # if not os.path.exists(path):
    #     os.mkdir(path)



if __name__ == "__main__":
    asyncio.run(main())
