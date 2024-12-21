from django.urls import path
from . import company_controller

urlpatterns = [
    path('', company_controller.create_company, name='create_company'),
    path('list/', company_controller.list_companies, name='list_companies'),
    path('<int:company_id>/', company_controller.get_company, name='get_company'),
    path('<int:company_id>/update/', company_controller.update_company, name='update_company'),
    path('<int:company_id>/delete/', company_controller.delete_company, name='delete_company'),
] 