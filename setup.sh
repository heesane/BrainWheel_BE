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
cp ~/Python_BrainWheel_BE/docker-compose.yml ~/

# Grafana 권한 문제 해결
sudo chown -R 472:472 Python_BrainWheel_BE/data/grafana

# Docker-Compose
sudo docker-compose up -d

# NVM for Node.js Installation
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.36.0/install.sh | bash

source ~/.bashrc

echo EveryThing is Done.