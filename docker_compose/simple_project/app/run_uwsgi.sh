#!/usr/bin/env bash

set -e

while ! nc -z $POSTGRES_HOST $POSTGRES_PORT;
do
    sleep 0.1
done

python manage.py migrate
python manage.py collectstatic --noinput

python manage.py createsuperuser \
    --noinput \
    --username $DJANGO_SUPERUSER_USERNAME \
    --email $DJANGO_SUPERUSER_EMAIL \
    || true

uwsgi --strict --ini uwsgi/uwsgi.ini
