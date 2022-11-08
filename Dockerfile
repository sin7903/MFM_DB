FROM --platform=linux/amd64 python:3.9-slim-buster


# set work directory as MLOps
WORKDIR /MLOps

# copy file
COPY DB_MLE.py .
COPY requirements.txt .

# RUN 
RUN apt-get update -y && apt-get install -y gcc &&\
    pip install --upgrade pip &&\
    pip install --upgrade setuptools wheel  &&\
    pip install -r requirements.txt &&\
    chmod 744 DB_MLE.py

# Create table and Insert data
CMD ["python", "DB_MLE.py"]