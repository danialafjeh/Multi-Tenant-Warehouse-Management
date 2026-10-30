from django.urls import path
from . import views

urlpatterns = [
    path('', views.products_management_page, name='products_management_page'),
    path('add/', views.add_product_system, name='add_product_system'),
    path('edit/<int:pk>/', views.edit_product_system, name='edit_product_system'),
    path('delete/<int:pk>/', views.delete_product_system, name='delete_product_system'),
    path('categories/', views.categories_management, name='categories_management_page'),
    path('units-of-measure/', views.units_of_measure_management_page, name='units_of_measure_management_page'),
    path('units-of-measure/add/', views.add_unit_of_measure_system, name='add_unit_of_measure_system'),
    path('units-of-measure/edit/<int:pk>/', views.edit_unit_of_measure_system, name='edit_unit_of_measure_system'),
    path('units-of-measure/delete/<int:pk>/', views.delete_unit_of_measure_system, name='delete_unit_of_measure_system'),
        

]
