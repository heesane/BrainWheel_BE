# SIDE : Raspberry Pi
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

rasp_ip = get_local_ip_address()
if rasp_ip is None:
    print("라즈베리파이 IP 주소를 가져올 수 없습니다.")
else:
    print("라즈베리파이 IP 주소:", rasp_ip)
