from django.urls import path
from . import views

urlpatterns = [
    path('inventory/', views.inventory_management, name='inventory_management'),
    path('movements/', views.stock_movements_management, name='stock_movements_management')

]
