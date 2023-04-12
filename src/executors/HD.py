import nmap3
import threading


class HostDiscovery:
    def __init__(self):
        self.result = []
        self.lock = threading.Lock()

    def scan(self, hd_type: int, transports: list[int], address_list: list):
        cmd_args = HostDiscovery.get_cmd(hd_type, transports)
        addrs = ' '.join(address_list)
        try:
            self.nmap_start(addrs, cmd_args)
        except Exception as e:
            print(e.args)

    def nmap_start(self, address_str: str, args: str):
        scanner = nmap3.Nmap()
        result = scanner.scan_top_ports(address_str, args=args, default=1)
        with self.lock:
            self.result.append(result)

    @staticmethod
    def get_cmd(hd_type: int, transports: list[int]) -> str:
        cmd_list = []

        def get_type_connections():
            nonlocal transports
            if 0 in transports:
                cmd_list.append('-PS')
            if 1 in transports:
                cmd_list.append('-PE -PP -PM')
            if 2 in transports:
                cmd_list.append('-PR')

        def get_type_scan():
            match hd_type:
                case 0:  # Only host scan
                    cmd_list.append('-sn')
                case 1:  # OS identification
                    cmd_list.append('-A')  # or -O (-A more informed)
                case 2:  # Port scan common
                    cmd_list.append('-F')
                case 3:  # All ports
                    cmd_list.append('-p-')

        get_type_scan()
        get_type_connections()

        cmd_str = ' '.join(cmd_list)
        return cmd_str
