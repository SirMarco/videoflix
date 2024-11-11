#!/bin/bash
if [ "$RUN_MIGRATIONS" = "true" ]; then
    python manage.py makemigrations
    python manage.py migrate
    python manage.py collectstatic --noinput
fi

# Startet den angegebenen Hauptprozess
exec "$@"
