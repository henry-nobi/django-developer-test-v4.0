from django.urls import path
from app.features.v1.user.user_controller import (
    get_user,
    update_user,
    delete_user,
    get_current_user,
    change_password,
    get_user_profiles,
)

urlpatterns = [
    path('<int:user_id>/', get_user, name='api-get-user'),
    path('<int:user_id>/update/', update_user, name='api-update-user'),
    path('<int:user_id>/delete/', delete_user, name='api-delete-user'),
    path('me/', get_current_user, name='get_current_user'),
    path('change-password/', change_password, name='change_password'),
    path('profiles/', get_user_profiles, name='get_user_profiles'),
]