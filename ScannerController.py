import os
from Scanners import *
from ScannerInfoManager import Manager
from datetime import datetime

scanners_by_scan_type = {
    0: HostDiscoveryScanner(),
    1: VulnerabilitiesScanner(),
}


class ScannerController:
    def __init__(self):
        self.path_results = f'{os.getcwd()}{os.sep}scan_results'
        if not os.path.exists(self.path_results):
            os.mkdir(self.path_results)

    # receive request and create a correct scanner. Then call this func and give a realized IScanner object to running
    def start_scan(self, body: dict):
        for i, host in enumerate(body['hosts']):
            info_dict = {}
            temp_res = None
            try:
                info_dict = {'host': host, 'dt_start': datetime.now().__str__(), 'dt_finish': '', 'status': ''}
                temp_res = scanners_by_scan_type.get(body['scan_type']).scan(host, body)
                info_dict['dt_finish'] = datetime.now().__str__()
                info_dict['status'] = 'Finished'
            except Exception as e:
                print(f'Error while scanning\n{e}')
                info_dict['dt_finish'] = datetime.now().__str__()
                info_dict['status'] = 'Error'
            finally:
                Manager.write_result(self.path_results, info_dict, temp_res, body['title'], i)
                del temp_res
                print('Scanning has been done')