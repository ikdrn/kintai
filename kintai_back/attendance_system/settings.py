# ファイル: kintai_back/attendance_system/settings.py
import os
from pathlib import Path
from django.core.exceptions import ImproperlyConfigured

# プロジェクトのルートディレクトリ
BASE_DIR = Path(__file__).resolve().parent.parent

def get_env_variable(var_name, default=None, required=False):
    """
    環境変数を取得するヘルパー関数
    - var_name: 環境変数の名前
    - default: 環境変数が設定されていない場合のデフォルト値
    - required: True の場合、環境変数が設定されていなければエラーを発生させる
    """
    value = os.environ.get(var_name, default)
    if required and value is None:
        raise ImproperlyConfigured(f"環境変数 {var_name} が設定されていません。")
    return value

# SECRET_KEY は必ず環境変数から取得（本番環境では必須）
SECRET_KEY = get_env_variable('DJANGO_SECRET_KEY', required=True)

# DEBUG モードは環境変数から取得（"True" なら True、それ以外は False）
DEBUG = get_env_variable('DJANGO_DEBUG', default='False') == 'True'

# ALLOWED_HOSTS はカンマ区切りの文字列を環境変数から取得
ALLOWED_HOSTS = get_env_variable('DJANGO_ALLOWED_HOSTS', default='localhost').split(',')

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'attendance_app',  # 勤怠アプリ
    'corsheaders',     # django-cors-headers (CORS 対策)
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # CORS ミドルウェアは上位に配置
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'attendance_system.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # テンプレートディレクトリ
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

WSGI_APPLICATION = 'attendance_system.wsgi.application'

# Database 設定も環境変数から取得
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': get_env_variable('KINTAI_DB_NAME', required=True),
        'USER': get_env_variable('KINTAI_DB_USER', required=True),
        'PASSWORD': get_env_variable('KINTAI_DB_PASSWORD', required=True),
        'HOST': get_env_variable('KINTAI_DB_HOST', default='localhost'),
        'PORT': get_env_variable('KINTAI_DB_PORT', default='3306'),
    }
}

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
LANGUAGE_CODE = 'ja'
TIME_ZONE = 'Asia/Tokyo'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'

# デフォルトの自動フィールド
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# CORS の設定も環境変数から取得（カンマ区切り）
cors_origins = get_env_variable('DJANGO_CORS_ALLOWED_ORIGINS', default='http://localhost:8080')
CORS_ALLOWED_ORIGINS = [origin.strip() for origin in cors_origins.split(',')]
CORS_ALLOW_CREDENTIALS = True

MIGRATION_MODULES = {
    'attendance_app': None,
}
