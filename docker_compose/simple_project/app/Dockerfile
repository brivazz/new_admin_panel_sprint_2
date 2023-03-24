FROM python:3.10

WORKDIR /opt/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV UWSGI_PROCESSES 1
ENV UWSGI_THREADS 16
ENV UWSGI_HARAKIRI 240
ENV DJANGO_SETTINGS_MODULE 'example.settings'

COPY requirements.txt requirements.txt

RUN  mkdir -p /opt/app/static/ \
     && mkdir -p /opt/app/media/ \
     && pip install --upgrade pip \
     && pip install -r requirements.txt

COPY . ./

RUN addgroup --gid 1001 --system app \
    && adduser --no-create-home \
    --shell /bin/false --disabled-password \
    --uid 1001 --system --group app \
    && chown -R app:app /opt/app

USER app

ENTRYPOINT ["sh", "run_uwsgi.sh"]
