"""
Django settings for DevBrain backend.
"""

from pathlib import Path
import os
from datetime import timedelta

# Build paths
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables from .env file (if python-dotenv is installed)
try:
    from dotenv import load_dotenv
    load_dotenv(BASE_DIR / '.env')
except ImportError:
    # If dotenv not installed, try to manually load .env
    env_file = BASE_DIR / '.env'
    if env_file.exists():
        with open(env_file) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ.setdefault(key.strip(), value.strip())

SECRET_KEY = 'django-insecure-devbrain-dev-only-change-in-production'

DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'localhost:8000', '0.0.0.0', '*']

# CORS settings for frontend integration
CORS_ALLOWED_ORIGINS = [
    'http://localhost:5173',
    'http://localhost:3000',
    'http://127.0.0.1:5173',
]

CORS_ALLOW_CREDENTIALS = True

INSTALLED_APPS = [
    'daphne',
    'django.contrib.admin',       # <-- Added
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',    # <-- Added (Required for Admin)
    'django.contrib.messages',    # <-- Added (Required for Admin)
    'django.contrib.staticfiles', # <-- Added (Required for Admin styling)
    'rest_framework',
    'corsheaders',
    'api'
] 

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',  # <-- Added
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware', # <-- Added
    'django.contrib.messages.middleware.MessageMiddleware',    # <-- Added
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
] 

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',        # <-- Added
                'django.contrib.messages.context_processors.messages', # <-- Added
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'
ASGI_APPLICATION = 'config.asgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 100,
    'DEFAULT_FILTER_BACKENDS': ['rest_framework.filters.SearchFilter'],
}

# File upload settings
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
DATA_UPLOAD_MAX_MEMORY_SIZE = 10485760  # 10MB
FILE_UPLOAD_MAX_MEMORY_SIZE = 10485760  # 10MB

# Gemini API - Load from environment variable for security
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY', 'INSERT_API_KEY_HERE')
GEMINI_MODEL = 'gemini-2.5-flash'

# Knowledge base settings
KNOWLEDGE_BASE_DIR = BASE_DIR / 'knowledge_base'
KNOWLEDGE_BASE_DIR.mkdir(exist_ok=True)

SUPPORTED_FILE_TYPES = ['pdf', 'txt', 'md', 'docx']
