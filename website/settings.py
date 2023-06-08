"""
Django settings for website project.

Generated by 'django-admin startproject' using Django 4.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

TIME_ZONE = "Asia/Kolkata"


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-vorhrr+^uw*y0in+44*k@q9d@io)4-&b*jcbadvy*2$ur+9y@l"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
# allow all hosts
ALLOWED_HOSTS = ["127.0.0.1", ".vercel.app"]


# Application definition
SITE_ID = 1
SOCIALACCOUNT_LOGIN_ON_GET = True
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.google",
    "category",
    "store",
    "product",
    "cart",
    "order",
    "review",
    "django_cleanup.apps.CleanupConfig",
    "storages",
]

SOCIALACCOUNT_PROVIDERS = {
    "google": {
        "APP": {
            "client_id": "826094995012-s244o1udtf5nhmjom4s8ul8a0te4lcp1.apps.googleusercontent.com",
            "secret": "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",
            "key": "",
        },
        "SCOPE": [
            "profile",
            "email",
        ],
    }
}
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "website.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": ["templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "website.context_processors.get_constant_data",
                "category.context_processors.get_categories",
                "cart.context_processors.get_cart_items",
            ],
        },
    },
]

WSGI_APPLICATION = "website.wsgi.app"


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases


# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.sqlite3",
#         "NAME": BASE_DIR / "db.sqlite3",
#     },
# }

import dj_database_url

# neon db

# DATABASES = {
#     "default": dj_database_url.parse(
#         "postgres://dheereshagrwal:2hu3cpdHMlSR@ep-black-wind-718099.us-east-2.aws.neon.tech/neondb"
#     )
# }

# elephant sql

DATABASES = {
    "default": dj_database_url.parse(
        "postgres://xmeagvtv:UNkm5-rWLMN6FIRTdIb-YrYIUddwrG0E@lucky.db.elephantsql.com/xmeagvtv"
    )
}




# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Asia/Kolkata"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = "static/"

STATICFILES_DIRS = [BASE_DIR / "static"]
# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
)

LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_HOST_USER = "dheereshaggarwal@gmail.com"
EMAIL_HOST_PASSWORD = "gqzcwzucfuyzlwkx"
EMAIL_USE_TLS = True

AWS_ACCESS_KEY_ID = "AKIAW55SMZOJOMC63PEH"
AWS_SECRET_ACCESS_KEY = "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"
AWS_STORAGE_BUCKET_NAME = "test-dheeresh"
DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
STATICFILES_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
AWS_S3_CUSTOM_DOMAIN = "%s.s3.amazonaws.com" % AWS_STORAGE_BUCKET_NAME
