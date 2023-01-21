from elevate import elevate
from ScannerController import ScannerController

if __name__ == "__main__":
    # elevate()
    controller = ScannerController()
    body = {
        'host': '172.24.28.215',
        'scan_type': 1,
        'transport_type': 2,
        'user_login': 'scanner_user',
        'pwd_login': 'P@ssword12-'
    }
    controller.start_scan(body)
