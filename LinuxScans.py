import paramiko


class SshFuncPassword:

    @staticmethod
    def __connecting(host: str, user: str, password: str) -> paramiko.SSHClient:
        _ = paramiko.SSHClient()
        _.connect(
            hostname=host,
            username=user,
            password=password,
            port=22)
        # _.load_system_host_keys()
        # _.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        return _

    @staticmethod
    def exec_command(h: str, ud: dict):
        c = SshFuncPassword.__connecting(h, ud['user'], ud['password'])
        _, res, _ = c.exec_command('ip address')
        return c, res.read().decode('utf-8')


class SshFuncKey:

    @staticmethod
    def __connecting(host: str, user: str, pk: str, p_phrase: str = None) -> paramiko.SSHClient:
        _ = paramiko.SSHClient()
        _pk = paramiko.RSAKey.from_private_key_file(pk, p_phrase)
        _.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        _.connect(
            hostname=host,
            username=user,
            pkey=_pk,
            passphrase=p_phrase,
            port=22)

        return _

    @staticmethod
    def exec_command(h: str, ad: dict):
        c = SshFuncKey.__connecting(h, ad['user'], ad['p_key'], ad['passphrase'])
        _, res, _ = c.exec_command('ip address')
        return c, res.read().decode('utf-8')
