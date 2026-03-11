"""
Django settings for config project.
Generated with django CMS 4.1.2 and Bootstrap 5
"""

import os
from decouple import config
from pathlib import Path
        
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
# config/settings.py - TOUT EN HAUT DU FICHIER

# Monkey patch pour compatibilité Django 4.x
import django
from django.utils.translation import gettext_lazy

# Patch ugettext_lazy
if not hasattr(django.utils.translation, 'ugettext_lazy'):
    django.utils.translation.ugettext_lazy = gettext_lazy
    import sys
    sys.modules['django.utils.translation'].ugettext_lazy = gettext_lazy

print("✓ Monkey patch appliqué pour ugettext_lazy → gettext_lazy")

# Le reste de votre settings.py...
from decouple import config
from pathlib import Path
# ...
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY', default='django-insecure-change-me-in-production')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=True, cast=bool)

#ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1').split(',')
ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'meftp.gouv.ne', 'www.meftp.gouv.ne']

#============================================================================
# CONFIGURATION DE REDIS POUR LE CACHE
#============================================================================
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}
# Session backend avec Redis (optionnel)
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_CACHE_ALIAS = 'default'
# ============================================================================

# Application definition
INSTALLED_APPS = [
    # Django core
    'djangocms_admin_style',     # ⬅️ EN PREMIER
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.sitemaps',

    # django CMS core
    'cms',                        # ⬅️ ICI
    'menus',
    'treebeard',
    'sekizai',
    
    # Filer
    'filer',
    'easy_thumbnails',
    
    # Plugins
    'djangocms_text',
    'djangocms_link',
    'djangocms_file',
    'djangocms_picture',
    'djangocms_video',
    'djangocms_frontend',
     
    # Frontend components (uncomment as needed)
    'djangocms_frontend.contrib.accordion',
    'djangocms_frontend.contrib.alert',
    'djangocms_frontend.contrib.badge',
    'djangocms_frontend.contrib.card',
    'djangocms_frontend.contrib.carousel',
    'djangocms_frontend.contrib.collapse',
    'djangocms_frontend.contrib.content',
    'djangocms_frontend.contrib.grid',
    'djangocms_frontend.contrib.icon',
    'djangocms_frontend.contrib.image',
    'djangocms_frontend.contrib.jumbotron',
    'djangocms_frontend.contrib.link',
    'djangocms_frontend.contrib.listgroup',
    'djangocms_frontend.contrib.media',
    'djangocms_frontend.contrib.tabs',
    'djangocms_frontend.contrib.utilities',
    
    # SEO
    'meta',
    
    # Contact form
    'django_contact_form',
    
    # Your custom apps
    'core',
]

# Middleware configuration - ORDER IS IMPORTANT!
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'cms.middleware.user.CurrentUserMiddleware',
    'cms.middleware.page.CurrentPageMiddleware',
    'cms.middleware.toolbar.ToolbarMiddleware',
    'cms.middleware.language.LanguageCookieMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates',
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
                'django.template.context_processors.csrf',
                'cms.context_processors.cms_settings',
                'sekizai.context_processors.sekizai',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME', default='meftp_web_db'),
        'USER': config('DB_USER', default='meftp_web_user'),
        'PASSWORD': config('DB_PASSWORD', default='meftp_web_pw'),
        'HOST': config('DB_HOST', default='localhost'),
        'PORT': config('DB_PORT', default='5432'),
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
LANGUAGE_CODE = 'fr'
LANGUAGES = [
    ('fr', 'Français'),
    ('en', 'English'),
]
TIME_ZONE = 'Africa/Niamey'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Site framework
SITE_ID = 1

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'static'
STATICFILES_DIRS = [
    BASE_DIR / 'static_files',
]

# Media files (User uploaded content)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# ============================================================================
# DJANGO CMS CONFIGURATION
# ============================================================================

# Confirmation for CMS 4
CMS_CONFIRM_VERSION4 = True

# CMS Templates
CMS_TEMPLATES = [
    ('Site_web/home.html', "Page d'accueil"),
    ('Site_web/page.html', "Page standard"),
    ('Site_web/fullwidth.html', "Pleine largeur"),
]

# CMS Permissions
CMS_PERMISSION = True

# CMS Placeholder configuration
CMS_PLACEHOLDER_CONF = {
    'content': {
        'name': 'Contenu principal',
        'plugins': ['TextPlugin', 'PicturePlugin', 'LinkPlugin'],
        'limits': {'global': 10},
    },
    'sidebar': {
        'name': 'Barre latérale',
        'plugins': ['TextPlugin', 'LinkPlugin'],
        'limits': {'global': 5},
    },
    'footer_left': {
        'name': 'Pied de page gauche',
        'plugins': ['TextPlugin', 'LinkPlugin'],
        'limits': {'global': 3},
    },
    'footer_right': {
        'name': 'Pied de page droit',
        'plugins': ['TextPlugin'],
        'limits': {'global': 2},
    },
    'mission_text': {
        'name': 'Texte de la mission',
        'plugins': ['TextPlugin'],
        'limits': {'global': 3},
    },
    'vision_text': {
        'name': 'Texte de la vision',
        'plugins': ['TextPlugin'],
        'limits': {'global': 3},
    },
    'values_text': {
        'name': 'Texte des valeurs',
        'plugins': ['TextPlugin'],
        'limits': {'global': 3},
    },
}

# ============================================================================
# DJANGOCMS TEXT CONFIGURATION
# ============================================================================

# Choose your editor: 'tiptap' (modern, no direct HTML) or 'ckeditor4' (legacy)
DJANGOCMS_TEXT_EDITOR = "djangocms_text.contrib.tiptap.tiptap"
# If you need CKEditor 4 compatibility:
# INSTALLED_APPS += ['djangocms_text.contrib.text_ckeditor4']
# DJANGOCMS_TEXT_EDITOR = "djangocms_text.contrib.text_ckeditor4.ckeditor4"

# ============================================================================
# DJANGOCMS FRONTEND (Bootstrap 5)
# ============================================================================

DJANGOCMS_FRONTEND_GRID_SIZE = 12
DJANGOCMS_FRONTEND_THEME_COLOR = '#0d6efd'

# ============================================================================
# DJANGOCMS LINK CONFIGURATION
# ============================================================================

DJANGOCMS_LINK_TEMPLATES = [
    ('default', 'Par défaut'),
]

DJANGOCMS_LINK_ALLOWED_LINK_TYPES = [
    'internal_link',  # Pages internes
    'external_link',  # URLs externes
    'file_link',      # Fichiers (si django-filer est installé)
    'tel',            # Téléphone
    'mailto',         # Email
]

# ============================================================================
# DJANGO FILER & THUMBNAILS
# ============================================================================

FILER_CANONICAL_URL = 'media/'
THUMBNAIL_HIGH_RESOLUTION = True
THUMBNAIL_PROCESSORS = (
    'easy_thumbnails.processors.colorspace',
    'easy_thumbnails.processors.autocrop',
    'filer.thumbnail_processors.scale_and_crop_with_subject_location',
    'easy_thumbnails.processors.filters',
)

# ============================================================================
# DJANGO CONTACT FORM
# ============================================================================

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'  # For development
# For production:
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = config('EMAIL_HOST', default='smtp.gmail.com')
# EMAIL_PORT = config('EMAIL_PORT', default=587, cast=int)
# EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=True, cast=bool)
# EMAIL_HOST_USER = config('EMAIL_HOST_USER')
# EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
# DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL')

# ============================================================================
# DJANGO META (SEO)
# ============================================================================

META_SITE_PROTOCOL = 'http'  # or 'https'
META_USE_SITES = True
META_USE_OG_PROPERTIES = True
META_USE_TWITTER_PROPERTIES = True
META_USE_GOOGLE_PLUS_PROPERTIES = False

# ============================================================================
# REDIS CACHE (optional)
# ============================================================================

if config('REDIS_URL', default=None):
    CACHES = {
        'default': {
            'BACKEND': 'django_redis.cache.RedisCache',
            'LOCATION': config('REDIS_URL'),
            'OPTIONS': {
                'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            }
        }
    }
else:
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
            'LOCATION': 'unique-snowflake',
        }
    }



# Configuration du cache pour django CMS
CMS_CACHE_DURATIONS = {
    'menus': 0,
    'content': 0,
    'permissions': 0,
}
CMS_PAGE_CACHE = False
CMS_PLACEHOLDER_CACHE = False
CMS_PLUGIN_CACHE = False

# ============================================================================
# SECURITY SETTINGS (for production)
# ============================================================================

if not DEBUG:
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
else:
    X_FRAME_OPTIONS = 'SAMEORIGIN'