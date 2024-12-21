from django.urls import path, include

urlpatterns = [
    path('auth/', include('app.features.v1.auth.auth_route')),
    path('user/', include('app.features.v1.user.user_route')),
    path('companies/', include('app.features.v1.company.company_route')),
    path('profiles/', include('app.features.v1.user_profile.user_profile_route')),
]