import os
from datetime import datetime

from src.connection_manage import connect_to_controller
from src.scan_services import Request, run_cmd
from write_manage import path, write_result


def main():
    if not os.path.exists(path):
        os.mkdir(path)

    with connect_to_controller('localhost', 8082) as conn:
        while True:
            request = Request(conn.recv(1536).decode())
            if not request:
                break

            try:
                info = {
                    'host': request.host_address,
                    'dt_start': datetime.now().__str__(),
                    'dt_finish': '',
                    'status': ''
                }

                report = run_cmd(request)
                print(f'Error while scanning\n{e}')
                info['status'] = 'Finished'
            except Exception as e:
                print(f'Error while scanning\n{e}')
                info['status'] = 'Error'
            finally:
                info['dt_finish'] = datetime.now().__str__()
                write_result(info, report)
                print('Scanning has been done')



if __name__ == "__main__":
    body = {
        'title': 'test',
        'hosts': ['172.24.30.71'],
        'scan_type': 1,
        'platform': 0,
        'transport_type': 0,
        'ssh_key': None, #r'C:\Users\meteo\Documents\test_key_paramiko',
        'passphrase': None, #'daniil',
        'user_login': 'scan',
        'pwd_login': 'P@ssword12-'
    }
