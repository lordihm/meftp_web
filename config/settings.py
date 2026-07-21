"""
Django settings for config project.
Configuration complète pour django CMS 4.1.2 avec Bootstrap 5
"""

import os
from decouple import config
from pathlib import Path

#============================================================================
# Monkey patch pour compatibilité Django 4.x
# django CMS 4.1.2 utilise ugettext_lazy qui a été supprimé dans Django 4.x, on le redéfinit pour éviter les erreurs
#============================================================================
import django
from django.utils.translation import gettext_lazy

# Patch ugettext_lazy
if not hasattr(django.utils.translation, 'ugettext_lazy'):
    django.utils.translation.ugettext_lazy = gettext_lazy
    import sys
    sys.modules['django.utils.translation'].ugettext_lazy = gettext_lazy

print("✓ Monkey patch appliqué pour ugettext_lazy → gettext_lazy")
#............................................................................

BASE_DIR = Path(__file__).resolve().parent.parent

# Sécurité
SECRET_KEY = config('SECRET_KEY', default='django-insecure-change-me')
DEBUG = config('DEBUG', default=True, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost:8000,127.0.0.1:8000').split(',')
# config/settings.py
CSRF_TRUSTED_ORIGINS = [
    'http://localhost:8000',
    'http://127.0.0.1:8000',
]

# Si vous utilisez HTTPS en production
# CSRF_COOKIE_SECURE = True
# SESSION_COOKIE_SECURE = True
# config/settings.py

# ============================================================================
# APPLICATION DEFINITION
# ============================================================================

INSTALLED_APPS = [
    'djangocms_admin_style',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    
    # django CMS core
    'cms',
    'menus',
    'treebeard',
    'sekizai',
    
    # Fichiers et médias
    'filer',
    'easy_thumbnails',
    
    # Plugins CMS
    'djangocms_text',
    'djangocms_link',
    'djangocms_file',
    'djangocms_picture',
    'djangocms_video',
    'djangocms_frontend',
    
    # Composants frontend (décommentez selon les besoins)
    'djangocms_frontend.contrib.accordion',
    'djangocms_frontend.contrib.alert',
    'djangocms_frontend.contrib.card',
    'djangocms_frontend.contrib.carousel',
    'djangocms_frontend.contrib.grid',
    'djangocms_frontend.contrib.icon',
    'djangocms_frontend.contrib.image',
    'djangocms_frontend.contrib.link',
    'djangocms_frontend.contrib.tabs',
    
    # SEO
    'meta',
    
    # Formulaire de contact
    'django_contact_form',
    
    # Votre application
    'core',
]

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
        'DIRS': [BASE_DIR / 'templates'],
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
                'core.context_processors.logo_du_site',
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

SITE_ID = 1

# Static files
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'static'
STATICFILES_DIRS = [BASE_DIR / 'static_files',]

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ============================================================================
# DJANGO CMS CONFIGURATION
# ============================================================================

CMS_CONFIRM_VERSION4 = True
# Avant (trop restrictif) X_FRAME_OPTIONS = 'DENY'
# Après (autorisé pour la toolbar)
X_FRAME_OPTIONS = 'SAMEORIGIN'

CMS_TEMPLATES = [
    ('Site_web/home.html', "Page d'accueil"),
    ('Site_web/page.html', "Page standard"),
    ('Site_web/fullwidth.html', "Pleine largeur"),
    ('Site_web/annuaire_des_services.html', "Annuaire des services"), 
]

CMS_TOOLBAR_ENABLED = True # Affiche la barre d'outils pour les utilisateurs connectés
CMS_PERMISSION = True # Active la gestion des permissions pour les pages

CMS_CACHE_DURATIONS = {
    'menus': 0,  # Désactivé pour éviter les problèmes de cache
    'content': 60 * 5,
    'permissions': 60 * 60,
}

CMS_PLACEHOLDER_CONF = {
    #======= PLACEHOLDERS POUR LES COULEURS =======#
    'primary_color': {
        'name': 'Couleur primaire',
        'plugins': ['TextPlugin'],  # Permet d'ajouter du texte pour la couleur (ex: #F97316)
        'limits': {'global': 1},
        'default_plugins': [
            {
                'plugin_type': 'TextPlugin',
                'values': {
                    'body': '#F97316',  # Couleur orange par défaut
                },
            },
        ],
    },
    #======= PLACEHOLDERS POUR LE HERO CONTENU =======#
   'hero_content': {  
        'name': 'Contenu de la bannière',
        'plugins': ['TextPlugin', 'PicturePlugin', 'LinkPlugin'],
        'limits': {'global': 10},  # Limite à 5 blocs
    },
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
    'vision_text': {
        'name': 'Texte de la vision',
        'plugins': ['TextPlugin'],
        'limits': {'global': 5},
    },
    'mission_text': {
        'name': 'Texte de la mission',
        'plugins': ['TextPlugin'],
        'limits': {'global': 5},
    },
    'values_text': {
        'name': 'Texte des valeurs',
        'plugins': ['TextPlugin'],
        'limits': {'global': 5},
    },
    #======= PLACEHOLDERS POUR LES SLIDES =======#
    'slide_texte_fond': {
        'name': 'Slide texte avec fond',
        'plugins': ['SlideTexteFondPluginPublisher'],
        'limits': {'global': 10},  # Un seul slide
    },
    #======= PLACEHOLDERS POUR LES SERVICES =======#
    'introduction': {
        'name': 'Texte d\'introduction',
        'plugins': ['TextPlugin'],
        'limits': {'global': 3},
    },
    'cabinet': {
        'name': 'Cabinet du Ministre',
        'plugins': ['TextPlugin'],
        'limits': {'global': None},
    },
    'secretariat': {
        'name': 'Secrétariat Général',
        'plugins': ['TextPlugin'],
        'limits': {'global': 3},
    },
    'directions_centrales': {
        'name': 'Directions Centrales',
        'plugins': ['TextPlugin'],
        'limits': {'global': None},  # Pas de limite pour les directions centrales
    },
    'directions_regionales': {
        'name': 'Directions Régionales',
        'plugins': ['TextPlugin'],
        'limits': {'global': None},  # Pas de limite pour les directions régionales
    },
    'centres_formation': {
        'name': 'Centres de Formation',
        'plugins': ['TextPlugin'],
        'limits': {'global': None},  # Pas de limite pour les centres de formation
    },
}

# ============================================================================
# DJANGOCMS TEXT CONFIGURATION
# ============================================================================

DJANGOCMS_TEXT_EDITOR = "djangocms_text.contrib.tiptap.tiptap"

# ============================================================================
# DJANGOCMS FRONTEND (Bootstrap 5)
# ============================================================================

DJANGOCMS_FRONTEND_GRID_SIZE = 12
DJANGOCMS_FRONTEND_THEME_COLOR = '#F97316'

# ============================================================================
# DJANGO FILER & THUMBNAILS
# ============================================================================

THUMBNAIL_HIGH_RESOLUTION = True
THUMBNAIL_PROCESSORS = (
    'easy_thumbnails.processors.colorspace',
    'easy_thumbnails.processors.autocrop',
    'filer.thumbnail_processors.scale_and_crop_with_subject_location',
    'easy_thumbnails.processors.filters',
)

# ============================================================================
# DJANGO META (SEO)
# ============================================================================

META_SITE_PROTOCOL = 'http'
META_USE_SITES = True
META_USE_OG_PROPERTIES = True
META_USE_TWITTER_PROPERTIES = True

# ============================================================================
# DJANGO CONTACT FORM
# ============================================================================

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'