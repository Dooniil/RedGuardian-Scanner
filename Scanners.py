import nmap3
from WindowsScans import WmiFunc, WinrmFunc
from LinuxScans import SshFunc
from enum import Enum

from datetime import datetime
from IScanner import IScanner


class HostDiscoveryScanner(IScanner):

    def scan(self, body: dict) -> dict:
        networks: str = body['hosts'].strip().replace(',', ' ')

        nmap = nmap3.Nmap()
        result: dict = nmap.nmap_list_scan(networks, arg='-sS', args='-O')

        # deleting unnecessary keys and down hosts
        for key in ['runtime', 'stats', 'task_results']:
            result.pop(key)

        hosts_all: int = result.keys().__len__()

        # deleting down hosts
        for key, value in list(result.items()):
            if value['state']['state'] == 'down':
                result.pop(key)

        hosts_up: int = result.keys().__len__()

        # adding the information about task
        result['information'] = {
            'data': str(datetime.now()),
            'hosts_all': hosts_all,
            'hosts_up': hosts_up
        }
        return result


# class TransportWindows(Enum):
#     WMI = 0,
#     WinRM = 1,
#
#
# class TransportLinux(Enum):
#     SSH_PASSWORD = 0,
#     SSH_KEY = 1,


class Vulnerability:
    def __init__(self, id_cve: str, code_result: dict[str: dict[str: str]]):
        self.id: str = id_cve
        self.code_for_test: dict[str: str] = code_result

vuln_test_1_code = {'(Get-Service -Name Spooler).Status': 'Running'}
vuln_test_1 = Vulnerability('CVE-2021-34527', vuln_test_1_code)


#  TODO надо разбить на классы будет, или как-то, способы проверок в зависимости от уязвимости, ибо тут
#   мы используем один Win32, а в другой уязвимости будет другая API
class VulnerabilitiesScanner(IScanner):

    #   Для обновлений
    def scan(self, body: dict) -> any:
        user_data: dict = {
            'user': body['user_login'],
            'password': body['pwd_login'],
        }
        try:
            match (body['platform'], body['transport_type']):
                case (0, 0): # Windows & WMI
                    for host in body['hosts']:
                        res = WmiFunc.exec_command(host, user_data)
                        print(res)
                case (0, 1): # Windows & WinRM
                    for host in body['hosts']:
                        res = WinrmFunc.exec_command(host, user_data)
                        print(res)
                case (1, 0): # Linux & SSH & Password
                    access_data = {
                        'user': user_data['user'],
                        'password': user_data['password'],
                        'p_key': body['ssh_key'],
                        'passphrase': body['passphrase'] if body['passphrase'] else None,
                    }
                    for host in body['hosts']:
                        c, res = SshFunc.exec_command(host, access_data)
                        print(res)
                        c.close()
        except Exception as e:
            print(e)
