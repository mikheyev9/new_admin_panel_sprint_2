import logging

logger = logging.getLogger('django.request')

class LogClientIPMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip_address = x_forwarded_for.split(',')[0].strip()
        else:
            ip_address = request.META.get('REMOTE_ADDR', 'Unknown')

        logger.info(f"Request from IP: {ip_address}, Path: {request.path}")

        return self.get_response(request)