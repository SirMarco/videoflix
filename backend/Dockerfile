FROM python:3.12.3

WORKDIR /app

COPY . .

RUN apt-get update && apt-get install -y ffmpeg

RUN /usr/local/bin/python -m pip install --upgrade pip

RUN pip install -r requirements.txt

# RUN chmod +x /app/compose/run-rq.sh

# RUN chmod +x /app/compose/run-backend.sh

CMD [ "/app/compose/run-backend.sh" ]

EXPOSE 8000