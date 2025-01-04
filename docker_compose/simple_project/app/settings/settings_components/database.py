import os

from django.conf import settings

DATABASE_TYPE = os.getenv('DATABASE_TYPE')


match DATABASE_TYPE:
    case 'postgres':
        DATABASES = {
            'default': {
                'ENGINE': os.getenv('SQL_ENGINE'),
                'NAME': os.getenv('POSTGRES_DB'),
                'USER': os.getenv('POSTGRES_USER'),
                'PASSWORD': os.getenv('POSTGRES_PASSWORD'),
                'HOST': os.getenv('SQL_HOST'),
                'PORT': os.getenv('SQL_PORT'),
                'OPTIONS': {
                    'options': os.getenv('SQL_OPTIONS'),
                },
            }
        }
    case 'sqlite':
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': os.path.join(settings.BASE_DIR, 'db.sqlite3'),
            }
        }
    case _:
        raise ValueError(f"Unsupported DATABASE_TYPE: {DATABASE_TYPE}")
