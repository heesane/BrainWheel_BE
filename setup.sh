#!/bin/bash

# vsftpd 설치
sudo apt-get update -y
sudo apt-get install -y vsftpd 

# /etc/ftpusers에  ubuntu 유저 추가
sudo sh -c 'echo "ubuntu" >> /etc/ftpusers'

# /etc/vsftpd.conf에서  sftp_server부분 주석 해제
sudo sed -i -e '122s/^#//' -e '123s/^#//' -e '125s/^#//' /etc/vsftpd.conf
# vsftpd 서비스 재시작
sudo systemctl restart vsftpd

# local에 nodejs설치
echo Visit https://nodejs.org/en/download/ and get the link to the nodejs tarball
echo enter the link here. Can skip this Through Enter
read url 
if [ -z "$url" ]
then
    echo Skipping the node.js installation
else
    #wget https://nodejs.org/dist/v18.12.1/node-v18.12.1-linux-arm64.tar.xz
    fname=$(echo $url|awk -F'/' '{ print $NF }')
    rm $fname
    wget $url
    if [ $? -eq 0 ] 
    then
        echo good
        tar xvf $fname
        cd $(echo $fname|sed 's/.tar.xz$//' | sed 's/.tar.gz$//')
        rm CHANGELOG.md LICENSE README.md
        sudo cp -R * /usr/local
        cd -
        rm -rf $(echo $fname|sed 's/.tar.xz$//' | sed 's/.tar.gz$//')
        sudo npm -g i mqtt basic-auth body-parser cron-parser 
        sudo npm -g i express fs loader node-schedule redis request
    else
        echo not good
    fi
fi


# docker와 docker-compose 설치
sudo apt install docker -y

# docker 권한 추가
sudo usermod -aG docker ubuntu

# docker 재시작
sudo systemctl restart containerd
sudo systemctl restart docker.service

# docker compose 설치
sudo apt install docker-compose -y

# git clone 후, docker-compose를 ~/ 디렉토리로 이동
mv ~/Python_BrainWheel_BE/docker-compose.yml ~/

# Grafana 권한 문제 해결
sudo chown -R 472:472 Python_BrainWheel_BE/data/grafana

# Docker-Compose
sudo docker-compose up -d

# NVM for Node.js Installation
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.36.0/install.sh | bash


# NVM을 통해 Node.js LTS버전 설치 후 사용
cd Python_BrainWheel_BE/data/node
source ~/.bashrc

# 원활하게 사용하기 위해 Reboot 진행
sudo reboot && echo "System Restarting..."

# node LTS버전 설치 
nvm install --lts
nvm use --lts
npm i express cors swagger-ui-express mysql body-parser
cd ~

# docker-compose Daemon으로 시작
sudo docker-compose restart

#-------------------------------------------------------#
# sudo docker-compose up -d

# Docker container의 이름과 사용자 이름과 비밀번호 설정
# CONTAINER_NAME="mysql"
# LOGIN_PASSWORD="5499458kK@"
# USER_NAME="hhs1"
# USER_PASSWORD="hhs"
# DATABASE_NAME="test_db"

# Docker container에서 MySQL에 접속하여 새로운 사용자 및 데이터베이스 생성
# mysql_query="CREATE USER '${USER_NAME}'@'%' IDENTIFIED WITH mysql_native_password BY '${USER_PASSWORD}'; \
# CREATE DATABASE ${DATABASE_NAME}; \
# USE test_db;
# CREATE TABLE users ( \
#   id int NOT NULL AUTO_INCREMENT, \
#   username varchar(255) NOT NULL, \
#   password varchar(255) NOT NULL, \
#   phone_number varchar(255) NOT NULL, \
#   Is_active tinyint(1) NOT NULL DEFAULT '1', \
#   PRIMARY KEY (id) \
# ); \
# GRANT ALL PRIVILEGES ON ${DATABASE_NAME}.* TO '${USER_NAME}'@'%';"

# sudo docker exec -it ${CONTAINER_NAME} mysql -u root -p${LOGIN_PASSWORD} -e "${mysql_query}"

# Docker container에서 InfluxDB에 접속하여 새로운 사용자 mid 및 데이터베이스 useful 생성
# sudo docker exec -it influxdb influx

# SQL문
# CREATE USER mid5 WITH PASSWORD 'mid';
# CREATE DATABASE useful;
# USE useful;
# GRANT ALL PRIVILEGES ON useful TO mid5;
# exit


