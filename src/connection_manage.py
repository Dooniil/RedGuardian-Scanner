import socket


def connect_to_controller(controller_address: str, controller_port: int):
    scanner_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    scanner_socket.connect_ex((controller_address, controller_port))
    return scanner_socket


# def