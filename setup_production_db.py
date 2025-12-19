#!/usr/bin/env python3
"""
Setup production database with initial data
"""
import os
import django
import sys

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'event_system.settings')
django.setup()

from django.core.management import execute_from_command_line
from django.contrib.auth.models import User
from events.models import Category

def main():
    print("🔧 Setting up production database...")
    
    # Run migrations
    print("📊 Running migrations...")
    execute_from_command_line(['manage.py', 'migrate', '--noinput'])
    
    # Create superuser if needed
    print("👤 Creating superuser...")
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser(
            username='admin',
            email=os.environ.get('ADMIN_EMAIL', 'admin@momenta.zm'),
            password=os.environ.get('ADMIN_PASSWORD', 'admin123')
        )
        print("✅ Superuser created")
    else:
        print("✅ Superuser already exists")
    
    # Create default categories if none exist
    print("📁 Creating default categories...")
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
    
    print("🎉 Database setup complete!")

if __name__ == "__main__":
    main()