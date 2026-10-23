from django.urls import path
from . import views

urlpatterns = [
    path('', views.warehouses_management, name='warehouses_management')


]
