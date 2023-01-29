import json
import os


class Manager:
    @staticmethod
    def __get_path_scan_result(path_results: str, title: str, index: int) -> str:
        return os.sep.join([path_results, f'{title}_{index}']) + '.json'

    @staticmethod
    def write_result(path_results: str, info: dict, result: dict, title: str, index):
        try:
            with open(Manager.__get_path_scan_result(path_results, title, index), mode='w') as file:
                json.dump([info, result,], file, separators=(',', ':'))
        except Exception as e:
            print(f'Error while writing results\n{e}')
        finally:
            print('Writing has been done')