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


class TransportWindows(Enum):
    WMI = 0,
    WinRM = 1,


class TransportLinux(Enum):
    SSH = 0


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
                case (0, TransportWindows.WMI.value):
                    for host in body['hosts']:
                        res = WmiFunc.exec_command(host, user_data)
                case (0, TransportWindows.WinRM.value):
                    for host in body['hosts']:
                        res = WinrmFunc.exec_command(host, user_data)
                case (1, TransportLinux.SSH.value):
                    for host in body['hosts']:
                        res = SshFunc.exec_command(host, user_data)
        except Exception as e:
            print(e)
