import nmap3

from WindowsScans import WmiFunc, WinrmFunc
from LinuxScans import SshFunc
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


class Vulnerability:
    def __init__(self, id_cve: str, code_result: dict[str: dict[str: str]]):
        self.id: str = id_cve
        self.code_for_test: dict[str: str] = code_result


spooler = Vulnerability('CVE-2021-34527', {'(Get-Service -Name Spooler).Status': 'Running'})
list_vulnerabilities = [spooler]


class VulnerabilitiesScanner:

    def scan(self, host, body: dict) -> any:
        access_data: dict = {
            'user': body['user_login'],
            'password': body['pwd_login'],
            'p_key': body['ssh_key'],
            'passphrase': body['passphrase'] if body['passphrase'] else None,  # проверка будет на ресте
        }
        try:
            match (body['platform'], body['transport_type']):
                case (0, 0):  # Windows & WMI
                    res = WmiFunc.exec_command(host, access_data)
                    print(res)
                case (0, 1):  # Windows & WinRM
                        report = WinrmFunc.exec_command(host, access_data, list_vulnerabilities)
                case (1, 0):  # Linux & SSH & Password
                    c, res = SshFunc.exec_command(host, access_data)
                    print(res)
                    c.close()
        except Exception as e:
            print(e)
        finally:
            return report
