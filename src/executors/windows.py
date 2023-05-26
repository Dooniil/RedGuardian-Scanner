import winrm


def exec_command(target, login, password, scripts):
    session = winrm.Session(
        target,
        auth=(login, password),
        message_encryption='auto')

    # for scripts:
    #     cve, session.run_ps(cmd).std_out.decode('utf-8').strip()
