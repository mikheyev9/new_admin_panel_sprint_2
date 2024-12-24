import os
from uuid import uuid4


def person_photo_path(instance, filename):
    """Генерация пути для сохранения фото каждого пользователя"""
    ext = filename.split('.')[-1]
    filename = f"{uuid4()}.{ext}"
    return os.path.join('person_photos', str(instance.id), filename)
