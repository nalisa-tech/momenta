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
        'DIRS': [BASE_DIR / 'templates'],
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

# --- Installed Apps (Production - NO DEBUG TOOLS) ---
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'events',
]

# --- Authentication Redirect ---
LOGIN_URL = '/login/'
DEBUG = False  # Always False in production

ALLOWED_HOSTS = ['*']  # Railway will handle domain restrictions

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

ROOT_URLCONF = 'event_system.urls'
WSGI_APPLICATION = 'event_system.wsgi.application'

SECRET_KEY = os.getenv('SECRET_KEY', '(9nl9hazytjjz7fxy18zmy-uc**t7t^eqa2e(c=wcdjbz+%5d+')

# Database configuration - Railway PostgreSQL
DATABASE_URL = os.getenv('DATABASE_URL')
if DATABASE_URL:
    DATABASES = {
        'default': dj_database_url.parse(DATABASE_URL)
    }
else:
    # Fallback to SQLite (shouldn't happen in production)
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

# Email Configuration - Production
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'  # Safe for production
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
EMAIL_HOST_USER = 'nalisaimbula282@gmail.com'
DEFAULT_FROM_EMAIL = 'Momenta <nalisaimbula282@gmail.com>'
EMAIL_SUBJECT_PREFIX = '[Momenta] '
EMAIL_TIMEOUT = 60

# Security settings for production
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_HSTS_SECONDS = 31536000
SECURE_REFERRER_POLICY = 'same-origin'
SECURE_SSL_REDIRECT = True  # Railway handles HTTPS
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