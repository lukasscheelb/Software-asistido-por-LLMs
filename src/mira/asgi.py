"""ASGI config for MIRA."""

import os

from django.core.asgi import get_asgi_application


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mira.settings")

application = get_asgi_application()
