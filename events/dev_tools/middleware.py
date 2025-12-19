# events/dev_tools/middleware.py

import time
import logging
from django.conf import settings
from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger('events')

class PerformanceMonitoringMiddleware(MiddlewareMixin):
    """
    Middleware to monitor request performance and log slow requests
    """
    
    def process_request(self, request):
        if settings.DEBUG and getattr(settings, 'PERFORMANCE_MONITORING', {}).get('ENABLED'):
            request._performance_start_time = time.time()
    
    def process_response(self, request, response):
        if settings.DEBUG and hasattr(request, '_performance_start_time'):
            duration = time.time() - request._performance_start_time
            
            # Get threshold from settings
            threshold = getattr(settings, 'PERFORMANCE_MONITORING', {}).get('SLOW_REQUEST_THRESHOLD', 2.0)
            
            if duration > threshold:
                logger.warning(
                    f"🐌 SLOW REQUEST: {request.method} {request.path} took {duration:.2f}s "
                    f"(threshold: {threshold}s)"
                )
            
            # Add performance header for debugging
            response['X-Response-Time'] = f"{duration:.3f}s"
            
        return response


class DeveloperInfoMiddleware(MiddlewareMixin):
    """
    Middleware to add developer information to responses
    """
    
    def process_response(self, request, response):
        if settings.DEBUG:
            # Add developer headers
            response['X-Django-Version'] = getattr(settings, 'DJANGO_VERSION', 'Unknown')
            response['X-Debug-Mode'] = 'True'
            response['X-Developer-Tools'] = 'Enabled'
            
            # Add database query count if available
            from django.db import connection
            response['X-DB-Queries'] = str(len(connection.queries))
            
        return response