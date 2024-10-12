#!/bin/bash

# Sammle Migrations und wende sie an
echo "Applying migrations..."
python manage.py makemigrations --noinput
python manage.py migrate --noinput

# Sammle statische Dateien
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Starte Gunicorn
echo "Starting Gunicorn..."
gunicorn --workers=3 --bind=0.0.0.0:8000 videoflix.wsgi:application
