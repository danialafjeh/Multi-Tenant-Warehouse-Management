from django.urls import path
from . import views

urlpatterns = [
    path('members/', views.members_management_page, name='members_management_page'),
    path('members/add/', views.add_member_system, name='add_member_system'),
    path('members/remove/<int:user_id>/', views.remove_member_system, name='remove_member_system'),
    path('settings/', views.delete_organization_page, name='delete_organization_page'),
    path('settings/delete', views.delete_organization_system, name='delete_organization_system'),


]
