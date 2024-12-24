import os
from django.conf import settings

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(settings.BASE_DIR, 'staticfiles')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(settings.BASE_DIR, 'media')