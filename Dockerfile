FROM python:3
ENV PIP_DISABLE_PIP_VERSION_CHECK 1

WORKDIR /usr/src/app
COPY /backend/requirements.txt /usr/src/app
COPY /backend/start.sh /usr/src/app/start.sh

RUN apt-get update && apt-get install -y ffmpeg
RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN chmod +x /usr/src/app/start.sh

EXPOSE 8000

CMD ["/usr/src/app/start.sh"]