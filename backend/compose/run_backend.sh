# Start backend
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --noinput
gunicorn --workers=1 --bind=0.0.0.0:8000 videoflix.wsgi:application