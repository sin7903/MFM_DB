FROM --platform=linux/amd64 python:3.9-slim-buster


# environment
# ENV DOCKER_DEFAULT_PLATFORM=linux/amd64

# set work directory as MLOps
WORKDIR /MLOps

# copy file
COPY DB_MLE.py .
COPY requirements.txt .

# RUN 
RUN apt-get update -y && apt-get install -y gcc
RUN pip install --upgrade pip
RUN pip install --upgrade setuptools wheel
RUN pip install -r requirements.txt

# Create table and Insert data
# CMD ["nohup DB_MLE.py &"]