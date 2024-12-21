from django.urls import path
from . import user_profile_controller

urlpatterns = [
    path('', user_profile_controller.create_profile, name='create_profile'),
    path('<int:profile_id>/', user_profile_controller.get_profile, name='get_profile'),
    path('<int:profile_id>/update/', user_profile_controller.update_profile, name='update_profile'),
    path('<int:profile_id>/delete/', user_profile_controller.delete_profile, name='delete_profile'),
    path('user/<int:user_id>/', user_profile_controller.list_user_profiles, name='list_user_profiles'),
] 