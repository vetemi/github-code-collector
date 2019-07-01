FROM python:3.6-stretch

WORKDIR /code-collector

COPY . /code-collector

RUN pip install -r requirements.txt 
