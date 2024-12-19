"""
URL configuration for lab2 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from app.core.configs.swagger import schema_view
from rest_framework.authtoken import views
from django.shortcuts import redirect
from django.conf.urls.i18n import i18n_patterns
from django.utils.translation import gettext_lazy as _
import json

# Non-localized URLs (API and system URLs)
urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
    path('api/v1/', include('app.features.urls')),
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

# Add localized URLs - these will have language prefix
urlpatterns += i18n_patterns(
    path('<int:profile_index>/', include([
        path('', include('app.presentations.urls')),  # Include all presentation URLs under profile
    ])),
    path('', include('app.presentations.urls')),
    prefix_default_language=False
)