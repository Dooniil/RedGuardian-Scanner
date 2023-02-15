import json
import os

path = f'{os.getcwd()}{os.sep}scan_results'


def write_result(info: dict, report: dict):
    file_name = os.sep.join([path, info.get('host')]) + '.json'
    try:
        with open(file_name, mode='w') as file:
            json.dump([info, report], file, separators=(',', ':'))
    except Exception as e:
        print(f'Error while writing results\n{e}')
    finally:
        print('Writing has been done')