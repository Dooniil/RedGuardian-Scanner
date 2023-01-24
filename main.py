from elevate import elevate
from ScannerController import ScannerController

if __name__ == "__main__":
    # elevate()
    controller = ScannerController()
    body = {
        'hosts': ['172.24.30.71'],
        'scan_type': 1,
        'platform': 0,
        'transport_type': 1,
        'ssh_key': None, #r'C:\Users\meteo\Documents\test_key_paramiko',
        'passphrase': None, #'daniil',
        'user_login': 'scan',
        'pwd_login': 'P@ssword12-'
    }
    controller.start_scan(body)
