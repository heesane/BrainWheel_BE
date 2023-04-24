#!/bin/bash

# vsftpd ��ġ
sudo apt-get update
sudo apt-get install vsftpd

# /etc/ftpusers ���Ͽ� ubuntu ����� �߰�
sudo echo "ubuntu" >> /etc/ftpusers

# /etc/vsftpd.conf ���Ͽ��� sftp_server�� �ּ� ����
sed -i -e '122s/^#//' -e '123s/^#//' -e '125s/^#//' /etc/vsftpd.conf
# vsftpd ���� �����
sudo systemctl restart vsftpd

sudo apt install docker docker-compose
mv ~/Python_BrainWheel/docker-compose.yml ~/
sudo docker-compose up -d

