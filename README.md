# MFM_DB
MLOps for MLE - chapter1 DB

MLOps for MLE의 DB 챕터의 실습내용입니다.

# Docker file을 이용한 실행법

## postgres 서버 실행
1. 서버 이미지 가져오기

`docker pull postgres`

2. docker 실행

`docker run -p 5432:5432 --name postgres -e POSTGRES_PASSWORD=my-password -d postgres`

3. 컨테이너 진입

`docker exec -it postgres /bin/bash`

## 테이블 생성 및 기록 docker 이미지 생성
1. 이미지 생성

`docker build -t my-image-name .`

2. 컨테이너 실행

`docker run -it --name my-container-name -d my-image-name`

## 컨테이너 네트워크 설정
1. 네트워크 생성

`docker network create my-network-name`

2. 네트워크 연결

`docker network connect my-network-name my-container-name`

`docker network connect my-network-name postgres`

## 컨테이너 진입 및 실행
1. 컨테이너 진입

`docker exec -it db-table /bin/bash`

3. 파일 샐행

`python DB_MLE.py`

## psql을 이용한 확인
1. psql로 postgres 서버 진입

`psql -h localhost -p 5432 -U postgres`

2. 서버에서 테이블 확인

`SELECT * FROM iris_data;`

# 참고사항
m1 mac book pro에서 `psycopg2.OperationalError: SCRAM authentication requires libpq version 10 or above`에러 발생함.
build 단계에서 platform을 설정해 줘야 함

# Model Registry
## (1) MLflow Server 띄우기

1. mlruns 폴더 생성

`mkdir mlruns`

2. mlflow server 띄위기

`mlflow server \  
--backend-store-uri sqlite:///mlflow.db \
--default-artifact-root $(pwd)/mlruns`

 3. 웹사이트 확인
 
http://127.0.0.1:5000/


## (2),(3) 데이터 추출, 모델 학습 및 저장

1. requirement.txt 파일 실행

tracking-server 폴더에 들어있는 requirement.txt 파일 실행

`…/Model/tracking-server/pip install -r requirement.txt`

2. pytnon 스크립트 실행

`python train.py`

3. 웹 사이트 확인

http://127.0.0.1:5000/


## (4) Download Model from MLFlow

1. python 스크립트 실행

`python load.py —run-id run_id`