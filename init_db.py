#!/usr/bin/env python3
"""
Initialize database for Railway deployment
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'event_system.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    django.setup()
    
    from django.core.management import execute_from_command_line
    from django.db import connection
    
    print("🔧 Initializing database...")
    
    # Check if we can connect to database
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        print("✅ Database connection successful")
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        sys.exit(1)
    
    # Run migrations
    print("📊 Running migrations...")
    execute_from_command_line(['manage.py', 'migrate', '--noinput'])
    
    print("✅ Database initialized successfully!")
    
except Exception as e:
    print(f"❌ Database initialization failed: {e}")
    sys.exit(1)