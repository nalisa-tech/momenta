# 🔧 Momenta Developer Tools Guide

## Overview
Comprehensive web browser developer tools for the Momenta Event Management System, providing debugging, performance monitoring, and development utilities.

## 🚀 Quick Start

### 1. Install Developer Tools
```bash
# Install dependencies
pip install django-debug-toolbar django-extensions django-silk

# Setup developer tools
python manage.py setup_devtools --install-deps --create-superuser

# Run development server
python manage.py runserver
```

### 2. Access Developer Tools
- **Developer Dashboard**: http://localhost:8000/dev/dashboard/
- **Django Admin**: http://localhost:8000/admin/
- **Silk Profiler**: http://localhost:8000/silk/
- **Debug Toolbar**: Appears automatically on pages (right sidebar)

## 🛠️ Available Tools

### 1. Django Debug Toolbar
**Location**: Right sidebar on all pages (DEBUG mode only)

**Features**:
- SQL query analysis and optimization
- Template rendering information
- Cache usage statistics
- Signal monitoring
- Static files analysis

**Usage**:
- Automatically appears when DEBUG=True
- Click panels to expand detailed information
- Monitor SQL queries for N+1 problems
- Check template context and inheritance

### 2. Django Silk (Performance Profiler)
**Location**: `/silk/`

**Features**:
- Request/response profiling
- SQL query profiling
- Python code profiling
- Performance bottleneck identification
- Historical performance data

**Usage**:
```python
# Profile specific code blocks
from silk.profiling.profiler import silk_profile

@silk_profile(name='Custom Function')
def my_function():
    # Your code here
    pass
```

### 3. Developer Dashboard
**Location**: `/dev/dashboard/` (Staff users only)

**Features**:
- System information overview
- Database statistics
- Recent SQL queries
- Performance metrics
- Cache management
- Developer console

**Quick Actions**:
- Clear application cache
- Refresh system status
- View database statistics
- Monitor recent queries

### 4. Browser Developer Tools
**Activation**: Ctrl+Shift+D (toggle floating panel)

**Features**:
- JavaScript console with command execution
- AJAX request monitoring
- Performance metrics tracking
- Error logging and handling
- Memory usage monitoring

**Keyboard Shortcuts**:
- `Ctrl+Shift+D`: Toggle dev panel
- `Ctrl+Shift+C`: Clear console
- `Ctrl+Shift+P`: Show performance metrics

## 📊 Performance Monitoring

### Automatic Monitoring
The system automatically monitors:
- Page load times
- SQL query performance
- AJAX request duration
- Memory usage
- Resource loading times

### Performance Thresholds
- **Slow Queries**: > 500ms
- **Slow Requests**: > 2 seconds
- **Memory Warnings**: Configurable

### Custom Performance Monitoring
```javascript
// Measure function performance
MomentaDevTools.measurePerformance(() => {
    // Your code here
}, 'Custom Function Name');

// Log custom metrics
MomentaDevTools.log('Custom message', 'performance');
```

## 🔍 Debugging Features

### SQL Query Analysis
```python
# In Django shell_plus
from django.db import connection
print(connection.queries)  # View all queries

# Enable SQL logging
import logging
logging.getLogger('django.db.backends').setLevel(logging.DEBUG)
```

### Template Debugging
- Use Debug Toolbar's Template panel
- Check template context variables
- Monitor template inheritance chain
- Identify unused context variables

### AJAX Request Debugging
```javascript
// All AJAX requests are automatically logged
// Check Network tab in browser dev tools
// Monitor in Momenta dev panel

// Manual AJAX logging
fetch('/api/endpoint')
  .then(response => {
    MomentaDevTools.log('API response received', 'ajax');
    return response.json();
  });
```

## 🎯 Common Debugging Scenarios

### 1. Slow Page Loading
1. Check Debug Toolbar SQL panel for slow queries
2. Use Silk profiler for detailed analysis
3. Monitor Network tab for slow resources
4. Check Performance tab in browser dev tools

### 2. Database Issues
1. Review SQL queries in Debug Toolbar
2. Check for N+1 query problems
3. Use `select_related()` and `prefetch_related()`
4. Monitor database statistics in dev dashboard

### 3. JavaScript Errors
1. Open browser console (F12)
2. Use Momenta dev panel (Ctrl+Shift+D)
3. Check error logs in console tab
4. Monitor AJAX requests in network tab

### 4. Memory Leaks
1. Use Performance tab in browser dev tools
2. Monitor memory usage in Momenta dev panel
3. Check for event listener leaks
4. Profile JavaScript heap usage

## 🔧 Configuration

### Settings Configuration
```python
# settings.py
if DEBUG:
    # Debug Toolbar
    DEBUG_TOOLBAR_CONFIG = {
        'SHOW_TOOLBAR_CALLBACK': lambda request: True,
        'SHOW_COLLAPSED': False,
    }
    
    # Silk Configuration
    SILKY_PYTHON_PROFILER = True
    SILKY_INTERCEPT_PERCENT = 100
    
    # Performance Monitoring
    PERFORMANCE_MONITORING = {
        'ENABLED': True,
        'SLOW_QUERY_THRESHOLD': 0.5,
        'SLOW_REQUEST_THRESHOLD': 2.0,
    }
```

### Environment Variables
```bash
# .env file
DEBUG=True
DJANGO_LOG_LEVEL=DEBUG
PERFORMANCE_MONITORING=True
```

## 📱 Mobile Development

### Mobile Debugging
- Use Chrome DevTools for mobile debugging
- Enable remote debugging on mobile devices
- Use responsive design mode in browser
- Test touch events and gestures

### Mobile Performance
- Monitor mobile-specific performance metrics
- Check network usage on mobile connections
- Test offline functionality
- Optimize for mobile memory constraints

## 🚀 Production Considerations

### Security
- **Never enable developer tools in production**
- Set `DEBUG=False` in production
- Remove developer tool dependencies from production requirements
- Use separate settings files for development/production

### Performance Impact
- Debug Toolbar adds overhead to requests
- Silk profiler stores data in database
- Browser dev tools have minimal impact
- Disable all tools in production

## 📚 Advanced Usage

### Custom Debug Panels
```python
# Create custom debug toolbar panel
from debug_toolbar.panels import Panel

class CustomPanel(Panel):
    name = 'Custom'
    template = 'debug_toolbar/panels/custom.html'
    
    def generate_stats(self, request, response):
        # Custom statistics generation
        pass
```

### Performance Profiling
```python
# Profile specific views
from silk.profiling.profiler import silk_profile

@silk_profile(name='Event Detail View')
def event_detail(request, event_id):
    # View logic here
    pass
```

### Custom Logging
```python
import logging
logger = logging.getLogger('events')

def my_view(request):
    logger.debug('Debug message')
    logger.info('Info message')
    logger.warning('Warning message')
    logger.error('Error message')
```

## 🆘 Troubleshooting

### Common Issues

1. **Debug Toolbar Not Showing**
   - Check `DEBUG=True`
   - Verify `INTERNAL_IPS` includes your IP
   - Ensure middleware is properly configured

2. **Silk Not Working**
   - Run migrations: `python manage.py migrate`
   - Check database permissions
   - Verify middleware order

3. **Browser Dev Tools Not Loading**
   - Check JavaScript console for errors
   - Verify static files are served correctly
   - Ensure `DEBUG=True`

4. **Performance Issues**
   - Disable unnecessary debug panels
   - Reduce Silk intercept percentage
   - Clear old profiling data

### Getting Help
- Check Django Debug Toolbar documentation
- Review Silk profiler documentation
- Use Django shell_plus for debugging
- Monitor application logs

## 📈 Best Practices

1. **Use appropriate tools for each task**
   - SQL issues → Debug Toolbar
   - Performance → Silk Profiler
   - JavaScript → Browser DevTools
   - System overview → Developer Dashboard

2. **Monitor performance regularly**
   - Set up performance thresholds
   - Review slow queries weekly
   - Monitor memory usage trends
   - Track page load times

3. **Keep tools updated**
   - Update developer dependencies regularly
   - Review new features in tools
   - Adapt configuration as needed

4. **Document debugging processes**
   - Create debugging checklists
   - Document common issues and solutions
   - Share knowledge with team members

## 🎉 Conclusion

The Momenta Developer Tools provide a comprehensive debugging and performance monitoring solution for web development. Use these tools to:

- Identify and fix performance bottlenecks
- Debug complex application issues
- Monitor system health and metrics
- Optimize database queries and application code
- Improve overall development productivity

Happy debugging! 🚀