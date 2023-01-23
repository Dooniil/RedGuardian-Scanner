import paramiko


class SshFunc:

    @staticmethod
    def __connecting(host: str, user: str, password: str) -> paramiko.SSHClient:
        _ = paramiko.SSHClient()
        _.connect(
            hostname=host,
            username=user,
            password=password,
            port=22)
        _.load_system_host_keys()
        _.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        return _

    @staticmethod
    def exec_command(h: str, ud: dict):
        c = SshFunc.__connecting(h, ud['user'], ud['password'])
        _, res, _ = c.exec_command('ip address')
        c.close()

        return res.read()
