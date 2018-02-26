"""Edgefolio URL configuration."""

from django.contrib import admin
from django.urls import path

from edgefolio import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('excel', views.ExcelView.as_view(), name='excel'),
]
