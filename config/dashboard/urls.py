from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_management_page, name='dashboard_management_page')

]
