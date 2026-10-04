"""Server-rendered views for the MIRA web adapter."""

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def bandeja(request: HttpRequest) -> HttpResponse:
    return render(request, "mira_web/bandeja.html")
