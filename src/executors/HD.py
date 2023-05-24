import nmap3


class HostDiscovery:
    @staticmethod
    def scan(hd_type: int, transports: list[int], address_list: list):
        cmd_args = HostDiscovery.get_cmd(hd_type, transports)
        addresses = ' '.join(address_list)

        try:
            scanner = nmap3.Nmap()
            result = scanner.scan_top_ports(addresses, args=cmd_args, default=10)
            return result
        except Exception as e:
            print(e.args)

    @staticmethod
    def get_cmd(hd_type, transports: list[int]) -> str:
        cmd_list = []

        def get_type_connections():
            nonlocal transports
            if 0 in transports:
                cmd_list.append('-PS')
            if 1 in transports:
                cmd_list.append('-PE -PP -PM')
            if 2 in transports:
                cmd_list.append('-PU')

        def get_type_scan():
            match hd_type:
                case 0:  # Only host scan
                    cmd_list.append('-sn')
                case 1:  # OS identification
                    cmd_list.append('-O')  # or -O (-A more informed)
                case 2:  # Port scan common
                    cmd_list.append('-F')
                case 3:  # All ports
                    cmd_list.append('-p-')

        get_type_scan()
        get_type_connections()

        cmd_str = ' '.join(cmd_list)
        return cmd_str
