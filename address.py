import psutil


def choose_host():
    for values in psutil.net_if_addrs().values():
        print(values[1].address)
    return input('Choose address: ')


