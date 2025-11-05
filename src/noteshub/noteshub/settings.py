import os
from pathlib import Path
from dotenv import load_dotenv
import dj_database_url

import socket
import psycopg2
import psycopg2.extensions
import psycopg2.extras

# Load environment variables
load_dotenv()

# === BASE SETTINGS ===
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv("SECRET_KEY", "django-insecure-_bs^!qt3%-(46p0=!#!ezeyk5)gf*s!hv=(8r_o6hzdq_vr1xr")
DEBUG = os.getenv("DEBUG", "True") == "True"
ALLOWED_HOSTS = [
    "to-do-hub.onrender.com",
    "localhost",
    "127.0.0.1",
]

def force_ipv4():
    original_getaddrinfo = socket.getaddrinfo
    def getaddrinfo_ipv4(*args, **kwargs):
        return original_getaddrinfo(*args, family=socket.AF_INET, **kwargs)
    socket.getaddrinfo = getaddrinfo_ipv4

force_ipv4()

# === APPS ===
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third-party
    'rest_framework',
    'corsheaders',

    # Local apps
    'accounts',
    'notes',
    'tasks',
]

# === REST FRAMEWORK ===
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}

# === MIDDLEWARE ===
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',

    # CORS early in the stack
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # Whitenoise for static files
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

CORS_ALLOW_ALL_ORIGINS = True

# === URL & WSGI ===
ROOT_URLCONF = 'noteshub.urls'
WSGI_APPLICATION = 'noteshub.wsgi.application'

# === TEMPLATES ===
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
            ],
        },
    },
]

# === DATABASE (Auto-switch: Supabase / Local PostgreSQL) ===
if os.getenv("DATABASE_URL"):
    # Supabase / Render (Production)
    DATABASES = {
        'default': dj_database_url.config(
            default=os.getenv("DATABASE_URL"),
            conn_max_age=600,
            ssl_require=True  # Supabase needs SSL
        )
    }
else:
    # Local PostgreSQL (Development)
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.getenv('DB_NAME', 'noteshub_db'),
            'USER': os.getenv('DB_USER', 'postgres'),
            'PASSWORD': os.getenv('DB_PASSWORD', 'postgres'),
            'HOST': os.getenv('DB_HOST', '127.0.0.1'),
            'PORT': os.getenv('DB_PORT', '5432'),
        }
    }

CSRF_TRUSTED_ORIGINS = ["https://to-do-hub.onrender.com"]


# === PASSWORD VALIDATORS ===
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# === LANGUAGE / TIMEZONE ===
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_TZ = True

# === STATIC / MEDIA FILES ===
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Whitenoise optimized static storage
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# === DEFAULT FIELD ===
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
