#!/bin/bash

# vsftpd 설치
sudo apt-get update
sudo apt-get install vsftpd

# /etc/ftpusers 파일에 ubuntu 사용자 추가
sudo echo "ubuntu" >> /etc/ftpusers

# /etc/vsftpd.conf 파일에서 sftp_server를 주석 해제
sed -i -e '122s/^#//' -e '123s/^#//' -e '125s/^#//' /etc/vsftpd.conf
# vsftpd 서비스 재시작
sudo systemctl restart vsftpd

sudo apt install docker docker-compose
mv ~/Python_BrainWheel/docker-compose.yml ~/
sudo docker-compose up -d

