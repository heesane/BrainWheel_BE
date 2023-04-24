#!/bin/bash

# vsftpd 설치
sudo apt-get update -y
sudo apt-get install -y vsftpd 

# /etc/ftpusers에  ubuntu 유저 추가
sudo echo "ubuntu" >> /etc/ftpusers

# /etc/vsftpd.conf에서  sftp_server부분 주석 해제
sed -i -e '122s/^#//' -e '123s/^#//' -e '125s/^#//' /etc/vsftpd.conf
# vsftpd 서비스 재시작
sudo systemctl restart vsftpd

# docker와 docker-compose 설치
sudo apt install -y docker docker-compose
# git clone 후, docker-compose를 ~/ 디렉토리로 이동
mv ~/Python_BrainWheel/docker-compose.yml ~/
# docker-compose Daemon으로 시작
sudo docker-compose up -d

# Docker container의 이름과 사용자 이름과 비밀번호 설정
CONTAINER_NAME="mysql"
LOGIN_PASSWORD="5499458kK@"
USER_NAME="hhs"
USER_PASSWORD="hhs"
DATABASE_NAME="test_db"

# Docker container에서 MySQL에 접속하여 새로운 사용자 및 데이터베이스 생성
sudo docker exec -it ${CONTAINER_NAME} mysql -u root -p${LOGIN_PASSWORD} -e "
  CREATE USER '${USER_NAME}'@'%' IDENTIFIED WITH mysql_native_password BY '${USER_PASSWORD}';
  CREATE DATABASE ${DATABASE_NAME};
  CREATE TABLE users (
  id int NOT NULL AUTO_INCREMENT,
  username varchar(255) NOT NULL,
  password varchar(255) NOT NULL,
  phone_number varchar(255) NOT NULL,
  Is_active tinyint(1) NOT NULL DEFAULT '1',
  PRIMARY KEY (id)
    );
  GRANT ALL PRIVILEGES ON ${DATABASE_NAME}.* TO '${USER_NAME}'@'%';
  exit;
"
# Docker container에서 InfluxDB에 접속하여 새로운 사용자 mid 및 데이터베이스 useful 생성
sudo docker exec -it influxdb influx -execute "
  CREATE USER mid WITH PASSWORD 'mid';
  CREATE DATABASE useful;
  USE useful;
  GRANT ALL PRIVILEGES ON useful TO mid;
  exit;
"
