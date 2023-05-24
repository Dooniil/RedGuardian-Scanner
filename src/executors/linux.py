import paramiko
from src.scan_services import Request


def exec_command(data: Request):
    pk = data.host_connection_info.get('pk')
    p_phrase = data.host_connection_info.get('p_phrase')

    session = paramiko.SSHClient()
    session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    session.connect(
        hostname=data.host_address,
        username=data.host_connection_info.get('user'),
        password=data.host_connection_info.get('password'),
        pkey=paramiko.RSAKey.from_private_key_file(pk, ) if pk else None,
        passphrase=p_phrase,
        port=22,
        timeout=3)

    while data.commands:
        cve, cmd = data.commands.pop()
        _, output, _ = session.exec_command(cmd)
        yield cve, output.read().decode('utf-8')

    session.close()
