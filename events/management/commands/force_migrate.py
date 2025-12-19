from django.core.management.base import BaseCommand
from django.core.management import execute_from_command_line
from django.db import connection
import sys

class Command(BaseCommand):
    help = 'Force database migrations for Railway deployment'

    def handle(self, *args, **options):
        self.stdout.write("🔧 Forcing database migrations...")
        
        try:
            # Check database connection
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
            self.stdout.write("✅ Database connection successful")
        except Exception as e:
            self.stdout.write(f"❌ Database connection failed: {e}")
            return
        
        try:
            # Run migrations
            self.stdout.write("📊 Running migrations...")
            execute_from_command_line(['manage.py', 'migrate', '--noinput', '--verbosity=2'])
            self.stdout.write("✅ Migrations completed successfully")
            
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
                
                self.stdout.write(f"✅ Created {len(categories)} default categories")
            
        except Exception as e:
            self.stdout.write(f"❌ Migration failed: {e}")
            sys.exit(1)