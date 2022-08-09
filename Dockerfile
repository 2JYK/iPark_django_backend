FROM python:3.9.10-buster
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update -y
RUN apt-get upgrade -y
RUN apt-get install -y ffmpeg libgl1-mesa-glx

COPY requirements.txt /usr/src/app/

WORKDIR /usr/src/app
RUN pip install -r requirements.txt

COPY . /usr/src/app/ 