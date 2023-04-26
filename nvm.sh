# node LTS버전 설치 
echo Installing Node LTS Version

cd Python_BrainWheel_BE/data/node
nvm install --lts
nvm use --lts
npm i express cors swagger-ui-express mysql body-parser
cd ~

# docker-compose Daemon으로 시작
sudo docker-compose up -d