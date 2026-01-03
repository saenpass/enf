# enf/settings/prod.py
from .base import *

DEBUG = False

ALLOWED_HOSTS = [
    'domen.com',
    'www.domen.com',
]

CSRF_TRUSTED_ORIGINS = [
    'https://domen.com',
    'https://www.domen.com',
]

CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True

SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
