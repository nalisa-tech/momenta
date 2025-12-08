# Troubleshooting Guide

Common issues and their solutions for the Nalisa Event Management System.

## Installation Issues

### "pip is not recognized"
**Problem**: Python or pip not in PATH  
**Solution**:
```bash
# Reinstall Python and check "Add Python to PATH" during installation
# Or use full path:
C:\Users\YourName\AppData\Local\Programs\Python\Python312\Scripts\pip.exe install -r requirement.txt
```

### "No module named 'django'"
**Problem**: Django not installed  
**Solution**:
```bash
pip install Django
# Or install all requirements:
pip install -r requirement.txt
```

### "Pillow installation failed"
**Problem**: Missing C++ build tools  
**Solution**:
- Download and install Visual C++ Build Tools
- Or use pre-built wheel: `pip install Pillow --only-binary :all:`

## Database Issues

### "no such table: events_category"
**Problem**: Migrations not applied  
**Solution**:
```bash
python manage.py migrate
```

### "Database is locked"
**Problem**: SQLite database locked by another process  
**Solution**:
- Close any database browsers (DB Browser for SQLite)
- Restart the development server
- If persists, delete `db.sqlite3` and run migrations again

### "UNIQUE constraint failed"
**Problem**: Trying to create duplicate data  
**Solution**:
```bash
# Clear existing data and repopulate:
python manage.py flush
python manage.py populate_data
```

## Server Issues

### "Port 8000 is already in use"
**Problem**: Another process using port 8000  
**Solution**:
```bash
# Use a different port:
python manage.py runserver 8001

# Or find and kill the process (Windows):
netstat -ano | findstr :8000
taskkill /PID <process_id> /F
```

### "Server won't start"
**Problem**: Various configuration issues  
**Solution**:
```bash
# Check for errors:
python manage.py check

# Verify migrations:
python manage.py showmigrations

# Check Python version:
python --version  # Should be 3.8+
```

## Template Issues

### "TemplateDoesNotExist"
**Problem**: Template file missing or wrong path  
**Solution**:
- Verify template exists in `templates/` folder
- Check `TEMPLATES` setting in `settings.py`
- Ensure template name matches exactly (case-sensitive)

### "Static files not loading"
**Problem**: Static files configuration  
**Solution**:
```bash
# In development, Django serves static files automatically
# Verify STATIC_URL in settings.py
# Check browser console for 404 errors
```

## Authentication Issues

### "CSRF verification failed"
**Problem**: Missing CSRF token  
**Solution**:
- Ensure `{% csrf_token %}` is in all POST forms
- Check that `CsrfViewMiddleware` is in MIDDLEWARE
- Clear browser cookies and try again

### "User is not authenticated"
**Problem**: Login not working  
**Solution**:
- Verify username and password are correct
- Check that `AuthenticationMiddleware` is enabled
- Ensure `LOGIN_URL` is set correctly in settings

## Booking Issues

### "Only X seats available"
**Problem**: Not enough seats for booking  
**Solution**:
- Reduce number of tickets
- Choose different ticket type
- Admin can increase seat count in admin panel

### "Payment page not loading"
**Problem**: Missing POST data  
**Solution**:
- Ensure you're coming from the seat selection page
- Don't refresh the payment page
- Start booking process from event detail page

## Admin Panel Issues

### "Can't access admin panel"
**Problem**: No superuser created  
**Solution**:
```bash
python manage.py createsuperuser
# Follow prompts to create admin account
```

### "Admin styling broken"
**Problem**: Static files not loading  
**Solution**:
```bash
# Ensure DEBUG = True in development
# Check STATIC_URL in settings.py
```

## Image Upload Issues

### "Images not displaying"
**Problem**: Media files configuration  
**Solution**:
- Verify `MEDIA_URL` and `MEDIA_ROOT` in settings.py
- Check that media URL pattern is in urls.py
- Ensure `media/` folder exists and is writable

### "Upload failed"
**Problem**: Pillow not installed  
**Solution**:
```bash
pip install Pillow
```

## Performance Issues

### "Site is slow"
**Problem**: Database queries or large dataset  
**Solution**:
- Use `select_related()` and `prefetch_related()` in queries
- Add database indexes
- Consider pagination for large lists
- Use caching for frequently accessed data

## Development Issues

### "Changes not reflecting"
**Problem**: Browser cache or server not reloading  
**Solution**:
- Hard refresh browser (Ctrl+Shift+R or Cmd+Shift+R)
- Restart development server
- Clear browser cache
- Check that auto-reload is working (should see "Watching for file changes")

### "Import errors"
**Problem**: Module not found  
**Solution**:
```bash
# Verify you're in the correct directory:
cd C:\Users\Nalisa\Desktop\mike

# Check installed packages:
pip list

# Reinstall requirements:
pip install -r requirement.txt
```

## Data Issues

### "Sample data not loading"
**Problem**: populate_data command fails  
**Solution**:
```bash
# Check for errors in command output
# Verify migrations are applied:
python manage.py migrate

# Try manual creation via admin panel
```

### "Lost all data"
**Problem**: Database deleted or corrupted  
**Solution**:
```bash
# Recreate database:
python manage.py migrate
python manage.py populate_data
python manage.py createsuperuser
```

## Browser Issues

### "Styles not loading"
**Problem**: Tailwind CDN blocked or slow  
**Solution**:
- Check internet connection
- Try different browser
- Check browser console for errors
- Verify CDN link in base.html

### "JavaScript not working"
**Problem**: Script errors  
**Solution**:
- Open browser console (F12)
- Check for JavaScript errors
- Ensure jQuery/other libraries are loaded
- Clear browser cache

## Production Deployment Issues

### "DEBUG = False causes errors"
**Problem**: Missing static files or ALLOWED_HOSTS  
**Solution**:
```python
# In settings.py:
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']

# Collect static files:
python manage.py collectstatic
```

### "Database connection failed"
**Problem**: Production database configuration  
**Solution**:
- Verify database credentials
- Check database server is running
- Ensure database exists
- Check firewall rules

## Getting Help

If you can't resolve an issue:

1. **Check error messages carefully** - They usually indicate the problem
2. **Search the error** - Google the exact error message
3. **Check Django documentation** - https://docs.djangoproject.com/
4. **Review the code** - Compare with working examples
5. **Contact support**:
   - Email: nalisaimbula282@gmail.com
   - Phone: 0978308101

## Useful Commands for Debugging

```bash
# Check Django version
python -m django --version

# Check Python version
python --version

# List installed packages
pip list

# Check for project issues
python manage.py check

# View migrations status
python manage.py showmigrations

# Open Django shell for testing
python manage.py shell

# Run with verbose output
python manage.py runserver --verbosity 3

# Check database
python manage.py dbshell
```

## Reset Everything (Last Resort)

If nothing works, start fresh:

```bash
# 1. Delete database
del db.sqlite3

# 2. Delete migration files (keep __init__.py)
del events\migrations\0*.py

# 3. Recreate migrations
python manage.py makemigrations
python manage.py migrate

# 4. Repopulate data
python manage.py populate_data
python manage.py createsuperuser

# 5. Restart server
python manage.py runserver
```
