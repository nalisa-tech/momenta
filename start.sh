#!/bin/bash

# Exit on any error
set -e

echo "🚀 Starting Momenta Event Management System..."

# Run database migrations
echo "📊 Running database migrations..."
python manage.py migrate --noinput

# Create superuser if it doesn't exist (optional)
echo "👤 Creating superuser if needed..."
python manage.py shell -c "
from django.contrib.auth.models import User
import os
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser(
        username='admin',
        email=os.environ.get('ADMIN_EMAIL', 'admin@momenta.zm'),
        password=os.environ.get('ADMIN_PASSWORD', 'admin123')
    )
    print('✅ Superuser created: admin')
else:
    print('✅ Superuser already exists')
"

# Start the Gunicorn server
echo "🌐 Starting Gunicorn server..."
exec gunicorn event_system.wsgi:application --bind 0.0.0.0:8000 --workers 3 --timeout 120