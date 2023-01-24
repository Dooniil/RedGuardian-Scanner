from elevate import elevate
from ScannerController import ScannerController

if __name__ == "__main__":
    # elevate()
    controller = ScannerController()
    body = {
        'hosts': ['10.0.0.173'],
        'scan_type': 1,
        'platform': 1,
        'transport_type': 1,
        'ssh_key': r'C:\Users\Administrator\Downloads\ssh_new_key',
        'passphrase': 'danil',
        'user_login': 'redcheck-admin',
        'pwd_login': 'P@ssword12-'
    }
    controller.start_scan(body)
