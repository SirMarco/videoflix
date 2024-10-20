FROM python:3.12.3 as build

WORKDIR /usr/src/app

COPY . .

RUN apt-get update && apt-get install -y ffmpeg
RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN chmod +x /usr/src/app/start_service.sh

EXPOSE 8000

CMD ["/usr/src/app/start_service.sh"]