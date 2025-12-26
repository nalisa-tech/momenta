from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('events.urls')),
]

if settings.DEBUG:
    # Media files in development
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
    # Developer Tools URLs
    try:
        import debug_toolbar
        urlpatterns = [
            path('__debug__/', include(debug_toolbar.urls)),
        ] + urlpatterns
    except ImportError:
        pass
    
    # Only add Silk if it's actually installed and working
    if 'silk' in settings.INSTALLED_APPS:
        try:
            import silk
            urlpatterns += [
                path('silk/', include('silk.urls', namespace='silk')),
            ]
        except (ImportError, RuntimeError):
            pass
