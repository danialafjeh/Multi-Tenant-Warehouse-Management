from django.urls import path
from . import views

urlpatterns = [
    path('', views.products_management, name='products_management'),
    path('categories/', views.categories_management, name='categories_management')

]
