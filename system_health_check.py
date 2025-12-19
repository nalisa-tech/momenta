#!/usr/bin/env python3
"""
System Health Check for Momenta Event Management System
Identifies and reports all potential issues in the system
"""

import os
import sys
import django
from pathlib import Path

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'event_system.settings')
django.setup()

def check_database():
    """Check database connectivity and migrations"""
    print("🔍 Checking Database...")
    try:
        from django.db import connection
        from django.core.management import execute_from_command_line
        
        # Test database connection
        cursor = connection.cursor()
        cursor.execute("SELECT 1")
        print("✅ Database connection: OK")
        
        # Check migrations
        from django.core.management.commands.migrate import Command
        migrate_cmd = Command()
        
        # This will show if there are unapplied migrations
        try:
            execute_from_command_line(['manage.py', 'showmigrations', '--plan'])
            print("✅ Migrations status: Checked")
        except Exception as e:
            print(f"⚠️  Migration check warning: {e}")
            
    except Exception as e:
        print(f"❌ Database error: {e}")
        return False
    return True

def check_models():
    """Check if all models can be imported and are valid"""
    print("\n🔍 Checking Models...")
    try:
        from events.models import (
            Category, Event, UserProfile, Booking, 
            PaymentTransaction, EventGallery, Venue, Resource,
            VenueBooking, ResourceAllocation
        )
        
        # Test model creation (dry run)
        models = [Category, Event, UserProfile, Booking, PaymentTransaction, 
                 EventGallery, Venue, Resource, VenueBooking, ResourceAllocation]
        
        for model in models:
            try:
                model._meta.get_fields()
                print(f"✅ Model {model.__name__}: OK")
            except Exception as e:
                print(f"❌ Model {model.__name__}: {e}")
                return False
                
    except ImportError as e:
        print(f"❌ Model import error: {e}")
        return False
    return True

def check_views():
    """Check if all views can be imported"""
    print("\n🔍 Checking Views...")
    try:
        from events import views
        
        # List of expected view functions
        expected_views = [
            'home', 'event_detail', 'login_user', 'logout_user', 'register_user',
            'book_event', 'categories_with_events', 'events_list', 'select_seat',
            'payment_page', 'approve_payment', 'reject_payment', 'user_profile',
            'subscribe_newsletter', 'venues_list', 'venue_detail', 'resources_list',
            'facilities_public', 'facilities_dashboard', 'category_detail'
        ]
        
        for view_name in expected_views:
            if hasattr(views, view_name):
                print(f"✅ View {view_name}: OK")
            else:
                print(f"❌ View {view_name}: Missing")
                return False
                
    except ImportError as e:
        print(f"❌ Views import error: {e}")
        return False
    return True

def check_urls():
    """Check URL configuration"""
    print("\n🔍 Checking URLs...")
    try:
        from django.urls import reverse
        from django.test import Client
        
        # Test critical URLs
        critical_urls = [
            'events:home',
            'events:events_list', 
            'events:categories_with_events',
            'events:login',
            'events:register'
        ]
        
        for url_name in critical_urls:
            try:
                url = reverse(url_name)
                print(f"✅ URL {url_name}: {url}")
            except Exception as e:
                print(f"❌ URL {url_name}: {e}")
                return False
                
    except Exception as e:
        print(f"❌ URL configuration error: {e}")
        return False
    return True

def check_static_files():
    """Check static files configuration"""
    print("\n🔍 Checking Static Files...")
    try:
        from django.conf import settings
        
        # Check static directories
        static_root = Path(settings.STATIC_ROOT)
        static_dirs = settings.STATICFILES_DIRS
        
        print(f"✅ STATIC_ROOT: {static_root}")
        print(f"✅ STATICFILES_DIRS: {static_dirs}")
        
        # Check if logo exists
        logo_path = Path(static_dirs[0]) / 'images' / 'logo.png'
        if logo_path.exists():
            print("✅ Logo file: Found")
        else:
            print("⚠️  Logo file: Missing (but not critical)")
            
    except Exception as e:
        print(f"❌ Static files error: {e}")
        return False
    return True

def check_templates():
    """Check template configuration"""
    print("\n🔍 Checking Templates...")
    try:
        from django.template.loader import get_template
        
        # Test critical templates
        critical_templates = [
            'base.html',
            'home.html',
            'events/event_detail.html',
            'events/categories_with_events.html'
        ]
        
        for template_name in critical_templates:
            try:
                template = get_template(template_name)
                print(f"✅ Template {template_name}: Found")
            except Exception as e:
                print(f"❌ Template {template_name}: {e}")
                return False
                
    except Exception as e:
        print(f"❌ Template configuration error: {e}")
        return False
    return True

def check_email_configuration():
    """Check email configuration"""
    print("\n🔍 Checking Email Configuration...")
    try:
        from django.conf import settings
        from django.core.mail import get_connection
        
        print(f"✅ EMAIL_BACKEND: {settings.EMAIL_BACKEND}")
        print(f"✅ EMAIL_HOST: {settings.EMAIL_HOST}")
        print(f"✅ EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}")
        
        # Test email connection (don't actually send)
        connection = get_connection()
        print("✅ Email connection: Configured")
        
    except Exception as e:
        print(f"❌ Email configuration error: {e}")
        return False
    return True

def check_admin_configuration():
    """Check admin configuration"""
    print("\n🔍 Checking Admin Configuration...")
    try:
        from django.contrib import admin
        from events.admin import (
            CategoryAdmin, EventAdmin, BookingAdmin, 
            PaymentTransactionAdmin, UserProfileAdmin
        )
        
        # Check if models are registered
        registered_models = admin.site._registry.keys()
        print(f"✅ Registered admin models: {len(registered_models)}")
        
        for model in registered_models:
            print(f"✅ Admin: {model.__name__}")
            
    except Exception as e:
        print(f"❌ Admin configuration error: {e}")
        return False
    return True

def main():
    """Run all health checks"""
    print("🏥 MOMENTA SYSTEM HEALTH CHECK")
    print("=" * 50)
    
    checks = [
        check_database,
        check_models,
        check_views,
        check_urls,
        check_static_files,
        check_templates,
        check_email_configuration,
        check_admin_configuration
    ]
    
    results = []
    for check in checks:
        try:
            result = check()
            results.append(result)
        except Exception as e:
            print(f"❌ Check failed with exception: {e}")
            results.append(False)
    
    print("\n" + "=" * 50)
    print("📊 HEALTH CHECK SUMMARY")
    print("=" * 50)
    
    passed = sum(results)
    total = len(results)
    
    if passed == total:
        print(f"🎉 ALL CHECKS PASSED ({passed}/{total})")
        print("✅ System is healthy and ready for deployment!")
    else:
        print(f"⚠️  {passed}/{total} checks passed")
        print("🔧 Please fix the issues above before deployment")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)