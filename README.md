<h1>순서도</h1>

## Server Side 
-------
![BW_Server](https://user-images.githubusercontent.com/93089183/235358812-dc02065a-7cb3-4d86-b543-f0ec028b64fc.JPG)

## Device Side
-------
![BW_Device](https://user-images.githubusercontent.com/93089183/235358796-c220808d-cc96-4ec1-8c35-824b70559fa0.JPG)




Configure_h5 : h5 file을 기반으로 현재의 데이터의 정확도 판단

Generate_h5 : csv파일을 기반으로 h5 file을 생성한다

Learn : Generate 파일과 동일. 라이브러리

make_csv : Influxdb에 특정갯수만큼 가져와서 csv에 담아서 저장

Push_data : 특정 개수만큼 Influxdb에 전송

Rasp_ip : raspberry의 IP를 출력

Transmit : Raspberry의 IP로 h5 파일 전송


