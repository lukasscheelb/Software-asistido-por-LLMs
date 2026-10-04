"""Django settings for the local MIRA application."""

from pathlib import Path
import os


BASE_DIR = Path(__file__).resolve().parents[2]

# This known value is intentionally limited to the local, non-production starter.
SECRET_KEY = "mira-local-development-only"
DEBUG = True
ALLOWED_HOSTS = ["127.0.0.1", "localhost", "[::1]", "testserver"]

INSTALLED_APPS = [
    "django.contrib.contenttypes",
    "django.contrib.staticfiles",
    "mira.web.apps.MiraWebConfig",
    "mira.infrastructure.apps.InfrastructureConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
]

ROOT_URLCONF = "mira.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {},
    },
]

WSGI_APPLICATION = "mira.wsgi.application"
ASGI_APPLICATION = "mira.asgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.environ.get("MIRA_DB_PATH", BASE_DIR / "db.sqlite3"),
        "OPTIONS": {"timeout": 20},
        "TEST": {"NAME": BASE_DIR / "test.sqlite3"},
    }
}

LANGUAGE_CODE = "es-cl"
TIME_ZONE = "America/Santiago"
USE_I18N = True
USE_TZ = True

STATIC_URL = "/static/"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
