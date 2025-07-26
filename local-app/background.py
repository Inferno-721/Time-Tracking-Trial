import socket
import psutil

def get_ip():
    hostname = socket.gethostname()
    return socket.gethostbyname(hostname)

def get_mac():
    for iface, addrs in psutil.net_if_addrs().items():
        for addr in addrs:
            if addr.family == psutil.AF_LINK:
                return addr.address
    return None