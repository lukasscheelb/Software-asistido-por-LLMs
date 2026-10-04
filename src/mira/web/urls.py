"""Routes exposed by the MIRA web adapter."""

from django.urls import path

from mira.web import views


app_name = "web"

urlpatterns = [
    path("bandeja/", views.bandeja, name="bandeja"),
]
