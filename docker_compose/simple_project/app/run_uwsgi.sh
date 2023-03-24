#!/usr/bin/env bash

set -e
sleep 10

python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --noinput

python manage.py createsuperuser \
    --noinput \
    --username $DJANGO_SUPERUSER_USERNAME \
    --email $DJANGO_SUPERUSER_EMAIL

uwsgi --strict --ini uwsgi/uwsgi.ini
