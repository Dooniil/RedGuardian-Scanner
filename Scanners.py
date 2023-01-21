import nmap3
import wmi
import winrm
import paramiko
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


class Transport(Enum):
    WMI = 0,
    WinRM = 1,
    SSH = 2


# class TransportLinux(Enum):
#     SSH = 0


#  TODO надо разбить на классы будет, или как-то, способы проверок в зависимости от уязвимости, ибо тут
#   мы используем один Win32, а в другой уязвимости будет другая API
class VulnerabilitiesScanner(IScanner):

    #   Для обновлений
    def scan(self, body: dict) -> any:
        transport: int = body['transport_type']
        try:
            if transport == Transport.WMI.value:
                connection = wmi.WMI(computer=body['host'], user=body['user_login'], password=body['pwd_login'])
                query_result = connection.Win32_QuickFixEngineering()
                return {zip(
                    [i for i in range(0, len(query_result))],
                    [j.HotFixID for j in query_result])}
            elif transport == Transport.WinRM.value:
                connection = winrm.Session(
                    f'http://{body["host"]}:5985/wsman',
                    auth=(body['user_login'], body['pwd_login']),
                    server_cert_validation='ignore',
                    transport='ntlm',
                    message_encryption='auto')
                query_result = connection.run_ps('Get-HotFix').std_out.decode('utf-8')
                print(query_result)
            elif transport == Transport.SSH.value:
                connection = paramiko.SSHClient()
                connection.load_system_host_keys()
                connection.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                connection.connect(
                    hostname=body['host'],
                    username=body['user_login'],
                    password=body['pwd_login'],
                    port=22)
                _, stdout, _ = connection.exec_command('ip address')
                print(stdout.read())
                connection.close()
        except Exception as e:
            print(e)
