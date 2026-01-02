#!/usr/bin/env python3
"""
PythonAnywhere Setup Script for Nalisa13
Run this in PythonAnywhere Bash console after uploading files
"""
import os
import sys
import django
from pathlib import Path

def setup_pythonanywhere():
    print("🚀 Setting up Momenta Events for PythonAnywhere (Python 3.11)")
    print("=" * 60)
    
    # Setup Django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'event_system.settings')
    sys.path.append('/home/Nalisa13/momenta')
    
    try:
        django.setup()
        
        from django.core.management import execute_from_command_line
        from django.contrib.auth.models import User
        from events.models import Category
        
        print("📊 Running database migrations...")
        execute_from_command_line(['manage.py', 'migrate', '--noinput'])
        print("✅ Migrations completed")
        
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
        
        print("📂 Creating default categories...")
        categories = [
            {'name': 'Music', 'slug': 'music', 'description': 'Concerts, festivals, and musical performances'},
            {'name': 'Tech', 'slug': 'tech', 'description': 'Technology conferences, workshops, and seminars'},
            {'name': 'Food', 'slug': 'food', 'description': 'Food festivals, tastings, and culinary events'},
            {'name': 'Sports', 'slug': 'sports', 'description': 'Sports events, tournaments, and competitions'}
        ]
        
        for cat_data in categories:
            category, created = Category.objects.get_or_create(
                slug=cat_data['slug'],
                defaults={
                    'name': cat_data['name'],
                    'description': cat_data['description']
                }
            )
            if created:
                print(f"✅ Created category: {category.name}")
            else:
                print(f"✅ Category exists: {category.name}")
        
        print("🎨 Collecting static files...")
        execute_from_command_line(['manage.py', 'collectstatic', '--noinput', '--clear'])
        print("✅ Static files collected")
        
        print("\n🎉 PythonAnywhere setup complete!")
        print("=" * 50)
        print("Your website will be live at: https://Nalisa13.pythonanywhere.com/")
        print("Admin panel: https://Nalisa13.pythonanywhere.com/admin/")
        print("Login: admin / admin123")
        print("\nDon't forget to:")
        print("1. Configure WSGI file in Web tab")
        print("2. Set static files mapping")
        print("3. Set virtual environment path")
        print("4. Reload your web app")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    return True

if __name__ == '__main__':
    setup_pythonanywhere()