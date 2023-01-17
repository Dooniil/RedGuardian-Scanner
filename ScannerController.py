import os
from Scanners import HostDiscoveryScanner
from ScannerInfoManager import Manager

scanners_by_scan_type = {
    0: HostDiscoveryScanner(),
}


class ScannerController:
    def __init__(self):
        self.path_results = f'{os.getcwd()}{os.sep}scan_results'
        if not os.path.exists(self.path_results):
            os.mkdir(self.path_results)

    # receive request and create a correct scanner. Then call this func and give a realized IScanner object to running
    def start_scan(self, body: dict):
        try:
            temp_res = scanners_by_scan_type[body['scan_type']].scan(body)
            Manager.write_result(self.path_results, temp_res)
        except Exception as e:
            print(f'Error while scanning\n{e}')
        finally:
            del temp_res
            print('Scanning has been done')