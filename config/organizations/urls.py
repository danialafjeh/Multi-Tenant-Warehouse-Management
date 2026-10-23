from django.urls import path
from . import views

urlpatterns = [
    path('members/', views.members_management, name='members_management')

]
