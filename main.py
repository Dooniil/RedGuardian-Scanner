from elevate import elevate
from ScannerController import ScannerController

if __name__ == "__main__":
    elevate()
    controller = ScannerController()
    body = {'hosts': 'localhost', 'scan_type': 0}
    controller.start_scan(body)
