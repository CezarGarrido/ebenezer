"""
Django settings for ebenezer project.

Generated by 'django-admin startproject' using Django 4.2.20.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

import os
from pathlib import Path
import sys

if getattr(sys, 'frozen', False):
    BASE_DIR = Path(sys._MEIPASS)       # Usado para templates, static, etc.
    EXEC_DIR = Path(sys.executable).parent  # Diretório do executável (fora do pacote)
else:
    BASE_DIR = Path(__file__).resolve().parent.parent
    EXEC_DIR = BASE_DIR
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-*h#@-rpxqu9pa&e^+s3ue9#%##4*3wvd%_qjkm3p*!#=*dl@em'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ["*"]


# Application definition
MY_APPS = [
    'core',
    'donation'
]

INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
] + MY_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
]

ROOT_URLCONF = 'ebenezer.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, "templates")],  # Aponta para a pasta templates no projeto
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

WSGI_APPLICATION = 'ebenezer.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': EXEC_DIR / 'db.sqlite3',
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

LANGUAGE_CODE = 'pt-BR'

TIME_ZONE = 'America/Campo_Grande'

USE_I18N = True

USE_TZ = True

LOCALE_PATHS = [
    BASE_DIR / "locale",
]


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')  # ou outro caminho absoluto no sistema
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(EXEC_DIR, 'media')


# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

JAZZMIN_SETTINGS = {
    'site_title': 'Ebenezer',
    'site_header': 'Ebenezer',
    'site_brand': 'Ebenezer',
    'welcome_sign': 'Bem-vindo(a) ao Ebenezer',
    'copyright': '© Ebenezer LTDA',
    'site_logo': 'images/company/logo.jpg',
    'icons': {
        'auth': 'fas fa-users-cog',
        'auth.user': 'fas fa-user',
        'auth.Group': 'fas fa-user-friends',
        'core.Donor': 'fas fa-hand-holding-heart',
        'core.Employee': 'fas fa-id-badge',
        'core.Company': 'fas fa-building',
        'donation.Donation': 'fas fa-donate',
    },
    'search_model': ['core.Donor'],
    'show_ui_builder': False,  # Desativa o personalizador (menos “web-like”)
    'custom_js': 'js/main.js',
    'related_modal_active': True,
    'site_logo_classes': 'img-circle elevation-3',
    'navigation_expanded': True,
}

JAZZMIN_UI_TWEAKS = {
    'theme': 'cosmo',  # Mais sóbrio que yeti, lembra interface nativa
    'accent': 'accent-primary',
    'navbar': 'navbar-white navbar-light',
    'navbar_fixed': True,
    'no_navbar_border': True,
    'footer_fixed': True,
    'sidebar_fixed': True,
    'sidebar': 'sidebar-light-primary',  # Sidebar clara, visual “de painel”
    'sidebar_nav_flat_style': True,
    'sidebar_nav_child_indent': True,
    'sidebar_nav_legacy_style': False,
    'sidebar_nav_compact_style': True,  # Menor, mais “app”
    'layout_boxed': False,
    'body_small_text': False,
    'brand_small_text': False,
    'navbar_small_text': False,
    'footer_small_text': True,
    'dark_mode_theme': None,
    'related_modal_active': True,
    'button_classes': {
        'primary': 'btn-primary',
        'secondary': 'btn-secondary',
        'info': 'btn-info',
        'warning': 'btn-warning',
        'danger': 'btn-danger',
        'success': 'btn-success'
    }
}

X_FRAME_OPTIONS = 'SAMEORIGIN'