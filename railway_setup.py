#!/usr/bin/env python3
"""
Railway-specific database setup
"""
import os
import sys
import django
from pathlib import Path

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'event_system.settings')
sys.path.append(str(Path(__file__).parent))

try:
    django.setup()
    
    from django.core.management import execute_from_command_line
    from django.db import connection
    from django.contrib.auth.models import User
    
    print("🚀 Railway Database Setup")
    print("=" * 50)
    
    # Test database connection
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        print("✅ Database connection successful")
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        sys.exit(1)
    
    # Run migrations
    print("📊 Running migrations...")
    try:
        execute_from_command_line(['manage.py', 'migrate', '--noinput'])
        print("✅ Migrations completed")
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        # Try to create tables manually
        print("🔧 Attempting to create tables...")
        execute_from_command_line(['manage.py', 'migrate', '--run-syncdb', '--noinput'])
    
    # Create superuser
    print("👤 Creating superuser...")
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser(
            username='admin',
            email='admin@momenta.zm',
            password='admin123'
        )
        print("✅ Superuser created: admin/admin123")
    else:
        print("✅ Superuser already exists")
    
    # Create default categories
    from events.models import Category
    if not Category.objects.exists():
        categories = [
            {'name': 'Music Events', 'slug': 'music'},
            {'name': 'Tech Events', 'slug': 'tech'},
            {'name': 'Food & Dining', 'slug': 'food'},
            {'name': 'Sports Events', 'slug': 'sports'},
        ]
        
        for cat_data in categories:
            Category.objects.create(**cat_data)
        
        print(f"✅ Created {len(categories)} default categories")
    else:
        print("✅ Categories already exist")
    
    print("🎉 Railway setup complete!")
    
except Exception as e:
    print(f"❌ Setup failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)