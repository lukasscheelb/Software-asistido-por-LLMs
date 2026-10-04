"""Routes exposed by the MIRA web adapter."""

from django.urls import path

from mira.web import views


app_name = "web"

urlpatterns = [
    path(
        "casos/<str:case_id>/evidencia/<int:index>/", views.evidencia, name="evidencia"
    ),
    path("bandeja/", views.bandeja, name="bandeja"),
    path("ejecutar-f4/", views.ejecutar_f4, name="ejecutar_f4"),
    path("casos/<str:case_id>/", views.detalle_caso, name="detalle_caso"),
]
