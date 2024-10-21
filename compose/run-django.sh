#!/usr/bin/env bash
cd /app

python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic
gunicorn --workers=1 --bind=0.0.0.0:8000 videoflix.wsgi:application &
daphne -b 0.0.0.0 -p 8001 videoflix.asgi:application