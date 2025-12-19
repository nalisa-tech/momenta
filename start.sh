#!/bin/bash

# Exit on any error
set -e

echo "Starting Momenta Event Management System..."

# Initialize database for Railway
echo "Running Railway database setup..."
python railway_setup.py

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput --clear

# Create superuser if it doesn't exist
echo "Creating superuser if needed..."
python manage.py shell -c "
from django.contrib.auth.models import User
import os
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser(
        username='admin',
        email=os.environ.get('ADMIN_EMAIL', 'admin@momenta.zm'),
        password=os.environ.get('ADMIN_PASSWORD', 'admin123')
    )
    print('Superuser created: admin')
else:
    print('Superuser already exists')
" || echo "Superuser creation skipped"

# Start the Gunicorn server
echo "Starting Gunicorn server on port ${PORT:-8000}..."
exec gunicorn event_system.wsgi:application \
    --bind 0.0.0.0:${PORT:-8000} \
    --workers 2 \
    --timeout 120 \
    --access-logfile - \
    --error-logfile - \
    --log-level info