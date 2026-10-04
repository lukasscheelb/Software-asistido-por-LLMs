"""Django application configuration for the web adapter."""

from django.apps import AppConfig


class MiraWebConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "mira.web"
    label = "mira_web"
    verbose_name = "MIRA web"
