from django.urls import path
from . import views

urlpatterns = [
    path('members/', views.members_management_page, name='members_management_page'),
    path('members/add/', views.add_member_system, name='add_member_system')

]
