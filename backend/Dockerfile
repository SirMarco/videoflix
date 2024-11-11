FROM python:3.12.3

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

RUN apt-get update && apt-get install -y ffmpeg

COPY /compose/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]

CMD ["gunicorn", "--workers=1", "--bind=0.0.0.0:8000", "videoflix.wsgi:application"]

EXPOSE 8000

# FROM python:3.12.3

# WORKDIR /app

# COPY requirements.txt .

# RUN pip install --upgrade pip && pip install -r requirements.txt

# COPY . .

# RUN apt-get update && apt-get install -y ffmpeg

# RUN chmod +x /app/compose/run_backend.sh

# EXPOSE 8000

# CMD ["/app/compose/run_backend.sh"]
