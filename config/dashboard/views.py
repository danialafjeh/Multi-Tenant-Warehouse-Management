from django.shortcuts import render

# Create your views here.

def dashboard_management(request):
    return render(request, 'dashboard.html', {})
