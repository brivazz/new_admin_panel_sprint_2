#!/usr/bin/env bash

sleep 10
set -e

python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --noinput

python manage.py createsuperuser \
    --noinput \
    --username $DJANGO_SUPERUSER_USERNAME \
    --email $DJANGO_SUPERUSER_EMAIL \
    || true

uwsgi --strict --ini uwsgi/uwsgi.ini
