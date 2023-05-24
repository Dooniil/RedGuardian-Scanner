from src.executors.HD import HostDiscovery


class HostDiscoveryHandler:

    @staticmethod
    def filter_state(items):
        key, val = items
        if isinstance(val, dict):
            state_dict = val.get('state')
            if state_dict and state_dict.get('state') == 'up':
                return True
        return False

    @staticmethod
    def scan(task):
        hd_setting = task.get('settings')
        result = HostDiscovery.scan(
            hd_setting.get('type'),
            hd_setting.get('protocols'),
            hd_setting.get('subnets'),
        )
        result = dict(filter(HostDiscoveryHandler.filter_state, result.items()))
        return result
