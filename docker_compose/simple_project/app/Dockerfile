FROM python:3.13-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV UWSGI_PROCESSES 1
ENV UWSGI_THREADS 16
ENV UWSGI_HARAKIRI 240
ENV DJANGO_SETTINGS_MODULE "settings.settings"


RUN apk add --update alpine-sdk cmake make gcc libtool ca-certificates openssl-dev \
    zlib-dev jpeg-dev libffi-dev python3-dev curl bash


RUN curl -LsSf https://astral.sh/uv/install.sh | bash

ENV PATH="${PATH}:/root/.local/bin"

WORKDIR /opt/app

COPY requirements.txt requirements.txt
COPY uwsgi/uwsgi.ini uwsgi.ini
COPY uwsgi/logrotate/uwsgi.conf /etc/logrotate.d/uwsgi
COPY run_uwsgi.sh run_uwsgi.sh

RUN uv pip install --system -r requirements.txt

COPY . .

EXPOSE 8000

RUN addgroup -S www-data || true \
    && adduser -S -G www-data www-data || true \
    && chmod +x /opt/app/run_uwsgi.sh

ENTRYPOINT ["sh", "-c", "python manage.py collectstatic --noinput && python manage.py migrate && ./run_uwsgi.sh"]
