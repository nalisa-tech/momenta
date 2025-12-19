release: python manage.py migrate --noinput
web: python manage.py collectstatic --noinput && gunicorn event_system.wsgi:application --bind 0.0.0.0:$PORT --workers 2