FROM python:3
ENV PIP_DISABLE_PIP_VERSION_CHECK 1

WORKDIR /usr/src/app

RUN apt-get update && apt-get install -y ffmpeg

COPY /backend/requirements.txt /usr/src/app
RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY /backend/start.sh /usr/src/app/start.sh
RUN chmod +x /usr/src/app/start.sh

EXPOSE 8000

CMD ["/usr/src/app/start.sh"]

# COPY ./backend .

# CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]