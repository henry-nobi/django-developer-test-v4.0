from django.urls import path
from app.features.v1.auth.auth_controller import (
    login,
    register,
    reset_password_request,
    reset_password_confirm,
    refresh_token,
    logout,
)

urlpatterns = [
    path('login/', login, name='api-login'),
    path('register/', register, name='api-register'),
    path('reset-password/', reset_password_request, name='api-reset-password'),
    path('reset-password-confirm/', reset_password_confirm, name='api-reset-password-confirm'),
    path('refresh-token/', refresh_token, name='api-refresh-token'),
    path('logout/', logout, name='api-logout'),
]