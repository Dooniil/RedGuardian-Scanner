import winrm

from src.scan_services import Request


def exec_command(data: Request):
    session = winrm.Session(
        f'{data.host_address}:5985',
        auth=(data.host_connection_info.get('user'), data.host_connection_info.get('password')),
        server_cert_validation='ignore',
        transport='ntlm' if data.host_connection_info.get('domain') is None else 'kerberos',
        message_encryption='auto')

    while data.commands:
        cve, cmd = data.commands.pop()
        yield cve, session.run_ps(cmd).std_out.decode('utf-8').strip()
