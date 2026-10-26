from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page, name='home_page'),
    path('signup/', views.signup_system, name='signup_system'),
    path('login/', views.login_system, name='login_system'),
    path('logout/', views.logout_system, name='logout_system')

]
