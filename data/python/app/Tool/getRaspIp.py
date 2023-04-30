# SIDE : Raspberz
import socket

def get_local_ip_address():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        
    except socket.error:
        local_ip = None
        
    return local_ip