from django.core.signals import request_started
from django.dispatch import receiver
import logging

logger = logging.getLogger('django.request')


@receiver(request_started)
def log_client_ip(sender, environ, **kwargs):
    x_forwarded_for = environ.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip_address = x_forwarded_for.split(',')[0]
    else:
        ip_address = environ.get('REMOTE_ADDR', 'Unknown')

    logger.info(f"Request from IP: {ip_address}, Path: {environ.get('PATH_INFO')}")

