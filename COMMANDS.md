# Quick Reference Commands

## Development

### Start the server
```bash
python manage.py runserver
```

### Create a superuser (admin)
```bash
python manage.py createsuperuser
```

### Make migrations (after model changes)
```bash
python manage.py makemigrations
python manage.py migrate
```

### Populate sample data
```bash
python manage.py populate_data
```

### Open Django shell
```bash
python manage.py shell
```

## Database Management

### Reset database (WARNING: Deletes all data)
```bash
del db.sqlite3
python manage.py migrate
python manage.py populate_data
python manage.py createsuperuser
```

### Export data
```bash
python manage.py dumpdata events > backup.json
```

### Import data
```bash
python manage.py loaddata backup.json
```

## Useful Django Commands

### Check for issues
```bash
python manage.py check
```

### Collect static files (for production)
```bash
python manage.py collectstatic
```

### Run tests
```bash
python manage.py test
```

## Admin Panel

Access at: http://127.0.0.1:8000/admin/

Default sections:
- **Events** - Manage all events
- **Categories** - Manage event categories
- **Bookings** - View all ticket bookings
- **Users** - Manage user accounts

## Troubleshooting

### Port already in use
```bash
python manage.py runserver 8001
```

### Clear cache
```bash
python manage.py clearsessions
```

### View migrations
```bash
python manage.py showmigrations
```

### SQL for a migration
```bash
python manage.py sqlmigrate events 0001
```
