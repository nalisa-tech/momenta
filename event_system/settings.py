import os
import dj_database_url
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Define BASE_DIR at the top
BASE_DIR = Path(__file__).resolve().parent.parent

# --- Static Files (CSS, JS, Images) ---
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'  # For production
STATICFILES_DIRS = [BASE_DIR / 'events/static']

# Use WhiteNoise for static files in production
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# --- Media Files (Uploaded Images) ---
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# --- Templates Directory ---
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # Fixed: use Path consistently
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'events.admin.admin_dashboard_context',
            ],
        },
    },
]

# --- Installed Apps ---
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'events',   # ← THIS MUST BE HERE
]

# --- Authentication Redirect ---
LOGIN_URL = '/login/'
DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'

# --- Developer Tools (Only in DEBUG mode) ---
if DEBUG:
    INSTALLED_APPS += [
        'debug_toolbar',
        'django_extensions',
        'silk',
    ]

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',') if os.getenv('ALLOWED_HOSTS') else ['*']

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# --- Developer Tools Middleware (Only in DEBUG mode) ---
if DEBUG:
    MIDDLEWARE = [
        'silk.middleware.SilkyMiddleware',  # Performance profiling
        'debug_toolbar.middleware.DebugToolbarMiddleware',  # Debug toolbar
    ] + MIDDLEWARE

ROOT_URLCONF = 'event_system.urls'
WSGI_APPLICATION = 'event_system.wsgi.application'

SECRET_KEY = os.getenv('SECRET_KEY', '(9nl9hazytjjz7fxy18zmy-uc**t7t^eqa2e(c=wcdjbz+%5d+')

# Database configuration
DATABASE_URL = os.getenv('DATABASE_URL')
if DATABASE_URL:
    # Production database (PostgreSQL on Railway)
    DATABASES = {
        'default': dj_database_url.parse(DATABASE_URL)
    }
else:
    # Development database (SQLite)
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': str(BASE_DIR / 'db.sqlite3'),
        }
    }

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Africa/Lusaka'
USE_I18N = True
USE_TZ = True

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Mobile Money Configuration
MTN_NUMBER = os.getenv('MTN_NUMBER', '0767675748')
AIRTEL_NUMBER = os.getenv('AIRTEL_NUMBER', '0978308101')
ZAMTEL_NUMBER = os.getenv('ZAMTEL_NUMBER', '0956183839')

# Bank Transfer Configuration
BANK_NAME = os.getenv('BANK_NAME', 'Standard Chartered Bank')
BANK_ACCOUNT_NUMBER = os.getenv('BANK_ACCOUNT_NUMBER', '0152516138300')
BANK_ACCOUNT_NAME = os.getenv('BANK_ACCOUNT_NAME', 'Momenta')

# Email Configuration
# To send real emails, you MUST set up Gmail App Password:
# 1. Go to: https://myaccount.google.com/security
# 2. Enable 2-Step Verification
# 3. Go to: https://myaccount.google.com/apppasswords
# 4. Create app password for "Mail"
# 5. Replace 'YOUR_16_DIGIT_APP_PASSWORD' below with the generated password

# Email Configuration - Using tygayt625@gmail.com for sending emails
# Check if we have a valid Gmail App Password
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', '')

if EMAIL_HOST_PASSWORD and len(EMAIL_HOST_PASSWORD) == 16:
    # Real email sending with custom Gmail SMTP backend
    EMAIL_BACKEND = 'events.email_backend.GmailEmailBackend'
    print("EMAIL: Real email sending enabled with custom Gmail SMTP backend")
else:
    # Safe console mode
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
    print("EMAIL: Console mode (safe). Set EMAIL_HOST_PASSWORD in .env to enable real emails")

# Additional email settings for better compatibility
EMAIL_SSL_CERTFILE = None
EMAIL_SSL_KEYFILE = None

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
EMAIL_HOST_USER = 'nalisaimbula282@gmail.com'
DEFAULT_FROM_EMAIL = 'Momenta <nalisaimbula282@gmail.com>'
EMAIL_SUBJECT_PREFIX = '[Momenta] '
EMAIL_TIMEOUT = 60

# For testing only (prints to console instead of sending):
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Security settings for production
if not DEBUG:
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_REFERRER_POLICY = 'same-origin'
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

# Session settings
SESSION_COOKIE_AGE = 1209600  # 2 weeks
SESSION_EXPIRE_AT_BROWSER_CLOSE = False

# Logging configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
    },
}

# ============================
# DEVELOPER TOOLS CONFIGURATION
# ============================

if DEBUG:
    # --- Django Debug Toolbar Configuration ---
    DEBUG_TOOLBAR_CONFIG = {
        'SHOW_TOOLBAR_CALLBACK': lambda request: True,  # Always show in debug mode
        'SHOW_COLLAPSED': False,
        'SHOW_TEMPLATE_CONTEXT': True,
        'ENABLE_STACKTRACES': True,
    }
    
    # Internal IPs for debug toolbar
    INTERNAL_IPS = [
        '127.0.0.1',
        'localhost',
    ]
    
    # --- Django Silk Configuration (Performance Profiling) ---
    SILKY_PYTHON_PROFILER = True
    SILKY_PYTHON_PROFILER_BINARY = True
    SILKY_PYTHON_PROFILER_RESULT_PATH = BASE_DIR / 'profiles'
    SILKY_INTERCEPT_PERCENT = 100  # Profile 100% of requests in debug mode
    SILKY_MAX_REQUEST_BODY_SIZE = 1024 * 1024  # 1MB
    SILKY_MAX_RESPONSE_BODY_SIZE = 1024 * 1024  # 1MB
    SILKY_META = True
    
    # --- Django Extensions Configuration ---
    SHELL_PLUS_PRINT_SQL = True
    SHELL_PLUS_PRINT_SQL_TRUNCATE = 1000
    
    # --- Enhanced Logging for Development ---
    LOGGING['loggers'] = {
        'django.db.backends': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
        'events': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
        'silk': {
            'level': 'INFO',
            'handlers': ['console'],
            'propagate': False,
        },
    }
    
    # --- Performance Monitoring ---
    PERFORMANCE_MONITORING = {
        'ENABLED': True,
        'SLOW_QUERY_THRESHOLD': 0.5,  # Log queries slower than 500ms
        'SLOW_REQUEST_THRESHOLD': 2.0,  # Log requests slower than 2 seconds
    }
    
    print("Developer Tools Enabled:")
    print("   - Django Debug Toolbar")
    print("   - Django Silk (Performance Profiling)")
    print("   - Django Extensions")
    print("   - Enhanced SQL Logging")
    print("   - Performance Monitoring")