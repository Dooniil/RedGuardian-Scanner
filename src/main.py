import os
from datetime import datetime

from src.connection_manage import conn_to_controller
# from src.scan_services import Request, run_cmd
from write_manage import path, write_result
import asyncio


async def main():
    if not os.path.exists(path):
        os.mkdir(path)

    await conn_to_controller()
        # while True:
        #     request = Request(conn.recv(1536).decode())
        #     if not request:
        #         break
        #
        #     try:
        #         info = {
        #             'host': request.host_address,
        #             'dt_start': datetime.now().__str__(),
        #             'dt_finish': '',
        #             'status': ''
        #         }
        #
        #         report = run_cmd(request)
        #         print(f'Error while scanning\n{e}')
        #         info['status'] = 'Finished'
        #     except Exception as e:
        #         print(f'Error while scanning\n{e}')
        #         info['status'] = 'Error'
        #     finally:
        #         info['dt_finish'] = datetime.now().__str__()
        #         write_result(info, report)
        #         print('Scanning has been done')


if __name__ == "__main__":
    asyncio.run(main())
