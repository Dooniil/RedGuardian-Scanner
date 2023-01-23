import wmi
import winrm


class WmiFunc:
    @staticmethod
    def __connecting(host: str, user: str, password: str) -> wmi.WMI:
        return wmi.WMI(computer=host, user=user, password=password)

    #  пока что только поиск обновления, потом буду разделять
    @staticmethod
    def exec_command(h: str, ud: dict):
        res = WmiFunc.__connecting(
            h, ud['user'], ud['password']
        ).Win32_QuickFixEngineering()
        return {zip(
            [i for i in range(0, len(res))],
            [j.HotFixID for j in res]
        )}


class WinrmFunc:
    @staticmethod
    def __connecting(host: str, user: str, password: str) -> winrm.Session:
        return winrm.Session(
                                f'http://{host}:5985/wsman',
                                auth=(user, password),
                                server_cert_validation='ignore',
                                transport='ntlm',
                                message_encryption='auto')

    #  пока что только поиск обновления, потом буду разделять
    @staticmethod
    def exec_command(h: str, ud: dict):
        return WinrmFunc.__connecting(
            h,
            ud['user'],
            ud['password']
        ).run_ps('Get-HotFix').std_out.decode('utf-8')
