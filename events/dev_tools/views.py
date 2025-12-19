# events/dev_tools/views.py

import json
import sys
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.admin.views.decorators import staff_member_required
from django.conf import settings
from django.db import connection
from django.core.cache import cache
from events.models import Event, Booking, PaymentTransaction, Category
from django.contrib.auth.models import User

@staff_member_required
def developer_dashboard(request):
    """
    Developer dashboard with system information and debugging tools
    """
    
    # System Information
    system_info = {
        'python_version': sys.version,
        'django_version': getattr(settings, 'DJANGO_VERSION', 'Unknown'),
        'debug_mode': settings.DEBUG,
        'database_engine': settings.DATABASES['default']['ENGINE'],
        'installed_apps': len(settings.INSTALLED_APPS),
        'middleware_count': len(settings.MIDDLEWARE),
    }
    
    # Database Statistics
    db_stats = {
        'total_queries': len(connection.queries),
        'users_count': User.objects.count(),
        'events_count': Event.objects.count(),
        'bookings_count': Booking.objects.count(),
        'payments_count': PaymentTransaction.objects.count(),
        'categories_count': Category.objects.count(),
    }
    
    # Recent Database Queries (last 10)
    recent_queries = connection.queries[-10:] if connection.queries else []
    
    # Performance Metrics
    performance_metrics = {
        'cache_enabled': bool(getattr(settings, 'CACHES', {})),
        'static_files_storage': settings.STATICFILES_STORAGE,
        'media_root': str(settings.MEDIA_ROOT),
        'static_root': str(settings.STATIC_ROOT),
    }
    
    context = {
        'system_info': system_info,
        'db_stats': db_stats,
        'recent_queries': recent_queries,
        'performance_metrics': performance_metrics,
        'settings_debug': settings.DEBUG,
    }
    
    return render(request, 'dev_tools/dashboard.html', context)


@staff_member_required
def api_inspector(request):
    """
    API endpoint for inspecting AJAX requests and responses
    """
    if request.method == 'POST':
        # Log API request for debugging
        data = json.loads(request.body)
        
        response_data = {
            'status': 'success',
            'message': 'API request logged',
            'request_data': data,
            'headers': dict(request.headers),
            'method': request.method,
            'path': request.path,
        }
        
        return JsonResponse(response_data)
    
    return JsonResponse({'error': 'Only POST requests allowed'})


@staff_member_required
def clear_cache(request):
    """
    Clear application cache
    """
    try:
        cache.clear()
        return JsonResponse({'status': 'success', 'message': 'Cache cleared successfully'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})


@staff_member_required
def system_status(request):
    """
    Get current system status as JSON
    """
    from django.db import connection
    
    status = {
        'database_connected': True,
        'cache_working': True,
        'debug_mode': settings.DEBUG,
        'query_count': len(connection.queries),
        'memory_usage': 'N/A',  # Could add psutil for memory monitoring
    }
    
    try:
        # Test database connection
        connection.ensure_connection()
    except Exception as e:
        status['database_connected'] = False
        status['database_error'] = str(e)
    
    try:
        # Test cache
        cache.set('test_key', 'test_value', 1)
        cache.get('test_key')
    except Exception as e:
        status['cache_working'] = False
        status['cache_error'] = str(e)
    
    return JsonResponse(status)