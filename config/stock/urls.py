from django.urls import path
from . import views

urlpatterns = [
    path('inventory/', views.inventory_management_page, name='inventory_management_page'),
    path('inventory/stock-in/', views.stock_in_system, name='stock_in_system'),
    path('inventory/stock-out/', views.stock_out_system, name='stock_out_system'),
    path('movements/', views.stock_movements_management, name='stock_movements_management')

]
