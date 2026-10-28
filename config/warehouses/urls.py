from django.urls import path
from . import views

urlpatterns = [
    path('', views.warehouses_management_page, name='warehouses_management_page'),
    path('add/', views.add_warehouse_system, name='add_warehouse_system'),
    path('edit/<int:warehouse_id>/', views.edit_warehouse_system, name='edit_warehouse_system'),



]
