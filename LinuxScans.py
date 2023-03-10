import paramiko


class SshFunc:

    @staticmethod
    def __connecting(host: str, access_data: dict) -> paramiko.SSHClient:
        user, password, pk, p_phrase = \
            access_data['user'], access_data['password'], access_data['p_key'], access_data['passphrase']
        _ = paramiko.SSHClient()
        _.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # if pk:
        #     _.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        _.connect(
            hostname=host,
            username=user,
            password=password,
            pkey=paramiko.RSAKey.from_private_key_file(pk, p_phrase) if pk else None,
            passphrase=p_phrase,
            port=22,
            timeout=3)
        # _.load_system_host_keys()

        return _

    @staticmethod
    def exec_command(h: str, access_data: dict):
        c = SshFunc.__connecting(h, access_data)
        _, res, _ = c.exec_command('ip address')

        return c, res.read().decode('utf-8')
