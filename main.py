from elevate import elevate
from ScannerController import ScannerController

if __name__ == "__main__":
    # elevate()
    controller = ScannerController()
    body = {'host': '10.0.0.147', 'scan_type': 1, 'transport_type': 0, 'user_login': '', 'pwd_login': 'P@ssword12-'}
    controller.start_scan(body)
