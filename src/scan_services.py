import json
from collections import deque
from src.executors.windows import exec_command as windows_exec_cmd
from src.executors.windows import exec_command as linux_exec_cmd


class Request:
    def __init__(self, req: str):
        self.__request_dict: dict = json.loads(req)
        self.host_address: str = self.__request_dict['connection_address']
        self.host_connection_info: dict = self.__request_dict['connection_info']
        self.commands: deque = deque()

        self.commands.extend(self.__request_dict['commands'])


def run_cmd(req: Request):
    conn_type = req.host_connection_info['connection_type']
    report = {}
    match conn_type:
        case 1:
            for cve, res_cmd in windows_exec_cmd(req):
                report[cve] = res_cmd
        case 2:
            for cve, res_cmd in linux_exec_cmd(req):
                report[cve] = res_cmd

    return report
