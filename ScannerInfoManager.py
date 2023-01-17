import json
import os
from datetime import datetime


class Manager:
    @staticmethod
    def __get_path_scan_result(path_results: str) -> str:
        file_name = datetime.now().__str__().replace(':', '-')
        return os.sep.join([path_results, file_name]) + '.json'

    @staticmethod
    def write_result(path_results: str, result: dict):
        try:
            with open(Manager.__get_path_scan_result(path_results), mode='w') as file:
                json.dump(result, file, separators=(',', ':'))
        except Exception as e:
            print(f'Error while writing results\n{e}')
        finally:
            print('Writing has been done')