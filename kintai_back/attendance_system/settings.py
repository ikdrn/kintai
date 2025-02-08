# kintai_back/attendance_system/settings.py

import os
from pathlib import Path

# プロジェクトのルートディレクトリ
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: 本番環境では秘密鍵は厳重に管理してください
SECRET_KEY = 'django.contrib.sessions.backends.signed_cookies'

# デバッグモード（開発時は True、本番では False）
DEBUG = True

# 許可するホスト（開発中は全て許可）
ALLOWED_HOSTS = ['*']


# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'attendance_app',      # 勤怠アプリ
    'corsheaders',         # django-cors-headers (CORS 対策)
]

MIDDLEWARE = [
    # CORS ミドルウェアはできるだけ上位に配置する必要があります
    'corsheaders.middleware.CorsMiddleware',
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
        # テンプレート用ディレクトリがある場合は指定します
        'DIRS': [BASE_DIR / 'templates'],
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


# Database
# 環境変数から MySQL 接続情報を読み込む（設定されていない場合はデフォルト値）
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('kintaiDB_NAME', 'testMySQL'),
        'USER': os.environ.get('kintaiDB_USER', 'root'),
        'PASSWORD': os.environ.get('kintaiDB_PASSWORD', 'oG-VtEz2#"rHEq9*'),
        'HOST': os.environ.get('kintaiDB_HOST', '35.187.220.47'),
        'PORT': os.environ.get('kintaiDB_PORT', '3306'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators
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
# https://docs.djangoproject.com/en/4.2/topics/i18n/
LANGUAGE_CODE = 'ja'
TIME_ZONE = 'Asia/Tokyo'
USE_I18N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/
STATIC_URL = '/static/'

# デフォルトの自動フィールド
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# CORS の設定
# クレデンシャル付きリクエストの場合、ワイルドカード（*）は利用できないため、
# 明示的にフロントエンドのオリジン（ここでは http://localhost:8080）を許可します。
CORS_ALLOWED_ORIGINS = [
    "http://localhost:8080",
]
CORS_ALLOW_CREDENTIALS = True

MIGRATION_MODULES = {
    'attendance_app': None,
}
