"""
Django settings for core project.
"""

import os
from pathlib import Path
from django.utils.translation import gettext_lazy as _

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# ==================================================================
# 🔒 SECURITY SETTINGS (Production Ready)
# ==================================================================

# SECRET_KEY من Environment Variable (آمن للـ Production)
SECRET_KEY = os.environ.get(
    'SECRET_KEY', 
    'django-insecure-your-secret-key-here-change-it-later'
)

# DEBUG = False في Production (آمن)
# بيقرأها من Environment Variable
DEBUG = os.environ.get('DEBUG', 'True') == 'True'

# ALLOWED_HOSTS بيقبل Railway + Ngrok + Localhost
ALLOWED_HOSTS = [
    '*',  # مؤقتاً للاختبار
    'localhost',
    '127.0.0.1',
    '.railway.app',  # كل subdomains of railway
    '.up.railway.app',
]

# CSRF Trusted Origins (Railway + Ngrok)
CSRF_TRUSTED_ORIGINS = [
    'https://jaws-premium-eclair.ngrok-free.dev',
    'https://*.ngrok-free.dev',
    'https://*.ngrok-free.app',
    'https://*.ngrok.io',
    'https://*.railway.app',
    'https://*.up.railway.app',
]

# ==================================================================
# 📦 Application Definition
# ==================================================================
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'accounts',
    'clinic',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # ✅ جديد: عشان Static Files
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'clinic.middleware.ForceClinicLanguageMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.i18n',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'clinic.context_processors.clinic_globals',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'

# ==================================================================
# 💾 Database Configuration
# ==================================================================
# لو Railway = PostgreSQL
# لو Local = SQLite

if 'DATABASE_URL' in os.environ:
    # Railway PostgreSQL
    try:
        import dj_database_url  # type: ignore[reportMissingImports]
    except ImportError as exc:
        raise ImportError(
            'dj_database_url is required when DATABASE_URL is set. '
            'Install it with `pip install dj-database-url`.') from exc

    DATABASES = {
        'default': dj_database_url.config(
            default=os.environ.get('DATABASE_URL'),
            conn_max_age=600,
        )
    }
else:
    # Local SQLite
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# ==================================================================
# 🔐 Password validation
# ==================================================================
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

# ==================================================================
# 🌍 Internationalization (i18n) & Localization (l10n)
# ==================================================================
LANGUAGE_CODE = 'en'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

LANGUAGES = [
    ('en', _('English')),
    ('ar', _('Arabic')),
]

LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale'),
]

# ==================================================================
# 📁 Static Files (CSS, JavaScript, Images)
# ==================================================================
STATIC_URL = '/static/'

# للـ Development
STATICFILES_DIRS = [BASE_DIR / 'static']

# للـ Production
STATIC_ROOT = BASE_DIR / 'staticfiles'

# WhiteNoise Configuration (لتحسين أداء Static Files)
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# ==================================================================
# 🖼️ Media Files
# ==================================================================
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ==================================================================
# ⚙️ Default primary key field type
# ==================================================================
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ==================================================================
# 👤 Custom User Model
# ==================================================================
AUTH_USER_MODEL = 'accounts.User'

# ==================================================================
# 🔄 Login/Logout Redirects
# ==================================================================
LOGIN_REDIRECT_URL = '/accounts/dashboard/'
LOGOUT_REDIRECT_URL = '/accounts/login/'

# ==================================================================
# 🔒 Security Settings (Production Only)
# ==================================================================
if not DEBUG:
    # HTTPS Settings
    SECURE_SSL_REDIRECT = False  # Railway بيتعامل مع HTTPS تلقائياً
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    
    # Cookies Security
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    
    # HSTS (يمنع الهجمات)
    SECURE_HSTS_SECONDS = 31536000  # سنة
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    
    # Content Security
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_BROWSER_XSS_FILTER = True
    X_FRAME_OPTIONS = 'DENY'