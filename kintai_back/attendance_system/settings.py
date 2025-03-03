# ファイル: kintai_back/attendance_system/settings.py
import os
import sys
import logging
from urllib.parse import urlparse, parse_qs

from django.core.exceptions import ImproperlyConfigured
from django.db import connections
from django.db.utils import OperationalError

# Configure logging
logger = logging.getLogger(__name__)

# -------------------------------------------------------------------
# Original GCP MySQL configuration
# (Keep this unchanged even if it expires; fallback happens at startup)
# -------------------------------------------------------------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': os.environ.get('GCP_MYSQL_HOST', 'your_gcp_mysql_host'),
        'USER': os.environ.get('GCP_MYSQL_USER', 'your_mysql_username'),
        'PASSWORD': os.environ.get('GCP_MYSQL_PASSWORD', 'your_mysql_password'),
        'NAME': os.environ.get('GCP_MYSQL_DB', 'your_mysql_database'),
        'PORT': os.environ.get('GCP_MYSQL_PORT', '3306'),
        # Additional options can be added here if needed.
    }
}

# -------------------------------------------------------------------
# Fallback to Neon PostgreSQL if the primary DB (GCP) has expired.
# A NEON_CONNECT environment variable is assumed available and set, e.g.:
# postgresql://neondb_owner:npg_PDYZ6yxk7ehQ@ep-flat-bar-a1nmau4p-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require
# -------------------------------------------------------------------

def parse_neon_dsn(dsn: str) -> dict:
    """
    Parse the DSN from NEON_CONNECT and return a Django DATABASE config.
    """
    result = urlparse(dsn)
    if result.scheme not in ('postgres', 'postgresql'):
        raise ImproperlyConfigured("NEON_CONNECT must be a PostgreSQL DSN")
    # Extract query parameters (for sslmode, etc.)
    query = parse_qs(result.query)
    # Django expects options with key sslmode, not as part of a query string.
    options = {}
    if 'sslmode' in query:
        options['sslmode'] = query['sslmode'][0]
    
    return {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': result.path.lstrip('/'),
        'USER': result.username,
        'PASSWORD': result.password,
        'HOST': result.hostname,
        'PORT': result.port or '5432',
        'OPTIONS': options,
    }

def try_connect_and_fallback():
    """
    Try to ensure connection to the configured default database.
    Fallback to Neon PostgreSQL if an OperationalError containing the error message '期限切れ'
    is encountered.
    """
    try:
        # Attempt to get a connection; this will trigger actual connection attempts
        connection = connections['default']
        connection.ensure_connection()
        logger.info("Successfully connected to GCP MySQL.")
    except OperationalError as e:
        error_message = str(e)
        if "期限切れ" in error_message:
            neon_dsn = os.environ.get("NEON_CONNECT")
            if neon_dsn:
                logger.warning("GCP MySQL connection error (期限切れ). Falling back to Neon PostgreSQL.")
                DATABASES['default'] = parse_neon_dsn(neon_dsn)
            else:
                logger.error("NEON_CONNECT environment variable not set. Cannot fallback to Neon PostgreSQL.")
        else:
            # For errors that are not the 'expired' one, re-raise the exception
            raise e

# Only attempt the connection when not running management commands that shouldn't connect to DB.
if 'runserver' in sys.argv or 'gunicorn' in sys.argv or 'uwsgi' in sys.argv:
    try_connect_and_fallback()

# -------------------------------------------------------------------
# Other Django settings below...
# (Include your INSTALLED_APPS, TEMPLATES, MIDDLEWARE, etc.)
# -------------------------------------------------------------------

DEBUG = os.environ.get('DEBUG', 'False') == 'True'

ALLOWED_HOSTS = ['*']  # Adjust as needed

INSTALLED_APPS = [
    # Your apps...
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # ...
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'kintai.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(os.path.dirname(__file__), 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'kintai.wsgi.application'

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'

# デフォルトの自動フィールド
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# CORS の設定：カンマ区切りの環境変数からリストに変換
cors_origins = get_env_variable('DJANGO_CORS_ALLOWED_ORIGINS', default='http://localhost:8080')
CORS_ALLOWED_ORIGINS = [origin.strip() for origin in cors_origins.split(',')]
CORS_ALLOW_CREDENTIALS = True

MIGRATION_MODULES = {
    'attendance_app': None,
}