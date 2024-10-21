FROM python:3.12.3 AS build

WORKDIR /app

COPY . .

RUN apt-get update && apt-get install -y ffmpeg

RUN /usr/local/bin/python -m pip install --upgrade pip

RUN pip install -r requirements.txt

EXPOSE 8000