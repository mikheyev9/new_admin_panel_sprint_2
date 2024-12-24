#!/usr/bin/env bash

set -e
# Устанавливаем текущую директорию как директорию скрипта
cd "$(dirname "$0")"

mkdir -p /var/log/uwsgi
chown -R www-data:www-data /var/log/uwsgi
chown -R www-data:www-data ./staticfiles
chown -R www-data:www-data ./media

uwsgi --strict --ini ./uwsgi.ini
