# events/dev_tools/urls.py

from django.urls import path
from . import views

app_name = 'dev_tools'

urlpatterns = [
    path('dashboard/', views.developer_dashboard, name='dashboard'),
    path('api-inspector/', views.api_inspector, name='api_inspector'),
    path('clear-cache/', views.clear_cache, name='clear_cache'),
    path('system-status/', views.system_status, name='system_status'),
]