#!/bin/bash

# vsftpd 설치
sudo apt-get update
sudo apt-get install vsftpd

# /etc/ftpusers에  ubuntu 유저 추가
sudo echo "ubuntu" >> /etc/ftpusers

# /etc/vsftpd.conf에서  sftp_server부분 주석 해제
sed -i -e '122s/^#//' -e '123s/^#//' -e '125s/^#//' /etc/vsftpd.conf
# vsftpd 서비스 재시작
sudo systemctl restart vsftpd

# docker와 docker-compose 설치
sudo apt install docker docker-compose
# git clone 후, docker-compose를 ~/ 디렉토리로 이동
mv ~/Python_BrainWheel/docker-compose.yml ~/
# docker-compose Daemon으로 시작
sudo docker-compose up -d

