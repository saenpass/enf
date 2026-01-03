# enf/settings/dev.py
from .base import *

DEBUG = True

ALLOWED_HOSTS = ['*']

CSRF_COOKIE_SECURE = False
SESSION_COOKIE_SECURE = False

SECURE_BROWSER_XSS_FILTER = False
SECURE_CONTENT_TYPE_NOSNIFF = False

CSRF_TRUSTED_ORIGINS = [
    'http://localhost:8000',
    'http://127.0.0.1:8000',
]

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
