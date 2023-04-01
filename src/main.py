import os

from connection_manage import run_server
# from write_manage import path, write_result
import asyncio

from src.address import choose_host


async def main():
    # if not os.path.exists(path):
    #     os.mkdir(path)
    host = choose_host()
    await run_server(host)

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
