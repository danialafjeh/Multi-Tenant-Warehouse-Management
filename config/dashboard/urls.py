from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_management, name='dashboard_management')

]
