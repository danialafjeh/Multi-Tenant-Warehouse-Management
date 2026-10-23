from django.shortcuts import render

# Create your views here.

def home_page(request):
    return render(request, 'home.html', {})



def login_system(request):
    return render(request, 'login.html', {})



def signup_system(request):
    return render(request, 'signup.html', {})


