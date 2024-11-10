FROM python:3.12.3

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

RUN apt-get update && apt-get install -y ffmpeg && apt-get clean

RUN chmod +x /app/compose/run-backend.sh

EXPOSE 8000

CMD ["/app/compose/run-backend.sh"]
