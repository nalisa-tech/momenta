#!/bin/bash

# Railway start script for Momenta
echo "Starting Momenta deployment..."

# Run migrations
python manage.py migrate --noinput

# Collect static files
python manage.py collectstatic --noinput

# Start gunicorn
exec gunicorn event_system.wsgi:application --bind 0.0.0.0:$PORT