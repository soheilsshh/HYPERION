from django.urls import path
from . import views


urlpatterns = [
    path('', views.service_list, name='service_list'), 
    path('add/', views.add_service, name='add_service'),
    path('edit/<int:pk>/', views.edit_service, name='edit_service'), 
    path('delete/<int:pk>/', views.delete_service, name='delete_service'),
]