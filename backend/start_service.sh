#!/bin/bash
python manage.py makemigrations --noinput
python manage.py migrate --noinput
python manage.py collectstatic --noinput
gunicorn --workers=3 --bind=0.0.0.0:8000 videoflix.wsgi:application &
# daphne -b 0.0.0.0 -p 8001 videoflix.asgi:application