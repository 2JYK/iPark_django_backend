FROM python:3.9.10-alpine
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apk update
RUN apk add build-base python3-dev py-pip jpeg-dev zlib-dev libpq-dev

COPY requirements.txt /usr/src/app/

WORKDIR /usr/src/app
RUN pip install -r requirements.txt

COPY . /usr/src/app/ 