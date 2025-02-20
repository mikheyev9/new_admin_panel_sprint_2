#!/bin/bash

# Директории, которые нужно создать
VOLUMES=(
  "./data/static"
  "./data/media"
  "./data/logs"
)


# Проверяем существование пользователя www-data
if ! getent group www-data > /dev/null; then
    echo "Создаём группу www-data..."
    groupadd -g 1000 www-data
else
    echo "Группа www-data уже существует"
fi

if ! getent passwd www-data > /dev/null; then
    echo "Создаём пользователя www-data..."
    useradd -u 1000 -g www-data -s /sbin/nologin www-data
else
    echo "Пользователь www-data уже существует"
fi

# UID и GID для пользователя www-data
WWW_DATA_UID=1000  # Замените на UID пользователя www-data из контейнера
WWW_DATA_GID=1000  # Замените на GID пользователя www-data из контейнера

# Создание директорий и установка прав
for DIR in "${VOLUMES[@]}"; do
  echo "Создаю директорию: $DIR"
  mkdir -p "$DIR"
  echo "Устанавливаю владельца $WWW_DATA_UID:$WWW_DATA_GID для $DIR"
  chown -R $WWW_DATA_UID:$WWW_DATA_GID "$DIR"
  echo "Устанавливаю права 775 для $DIR"
  chmod -R 775 "$DIR"
done

echo "Все директории подготовлены!"