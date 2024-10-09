FROM python:3

WORKDIR /usr/src/app

RUN apt-get update && apt-get install -y ffmpeg

COPY requirements.txt ./
RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# COPY ./backend .

CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]