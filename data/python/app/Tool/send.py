# SIDE : Server
import os
import paramiko

"""
기능 정리
1. Server단에서 각 Local의 Raspberry PI로 .h5 file 전송
2. Raspberry PI의 /home/pi/sp/h5_file 경로가 존재하지 않을 경우, 자동 생성

호출 방법
from learn_transmit.transmit import sftp_upload
sftp_upload("1.h5"(remote),"2.h5"(local))
"""

# remote : file_name (str)
# local : file_name (str)
def sftp_upload(remote, local):
    host = 'raspberrypi'
    port = 22
    userId = "pi"
    password = '0000' 
    localpath = os.path.dirname(os.path.abspath(__file__))+"\\h5_file\\"+local
    remotepath = '/home/pi/sp/h5_file/'+remote
    
    
    """
    SFTP를 사용하여 .h5 파일을 Raspberry PI에 업로드하는 함수

    Args:
        host (str): SFTP 호스트 주소
        port (int): SFTP 포트 번호
        userId (str): SFTP 접속 사용자 ID
        password (str): SFTP 접속 사용자 비밀번호
        remotepath (str): SFTP 서버의 원격 경로 (파일이 업로드 될 경로 및 파일 이름)
        localpath (str): 로컬 PC의 파일 경로 (업로드 할 파일 경로 및 파일 이름)

    Returns:
        None
    """
    try:
        # 연결
        transport = paramiko.Transport((host, port))
        transport.connect(username=userId, password=password)
        sftp = transport.open_sftp()
        
        # h5_file 폴더가 없으면 생성
        sftp.mkdir('/home/pi/sp/h5_file', mode=755, ignore_existing=True)
        
        # 파일 업로드
        sftp.put(localpath, remotepath)
        print(f"파일 업로드 완료: {localpath} -> {remotepath}")
        return 200

    except Exception as e:
        print(f"파일 업로드 실패: {e}")
        return 404
    
    finally:
        # 연결 종료
        sftp.close()
        transport.close()
        print("SFTP 연결 종료")


