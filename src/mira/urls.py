"""Root URL configuration for MIRA."""

from django.urls import include, path
from django.views.generic import RedirectView


urlpatterns = [
    path(
        "",
        RedirectView.as_view(pattern_name="web:bandeja", permanent=False),
        name="inicio",
    ),
    path("", include("mira.web.urls")),
]
