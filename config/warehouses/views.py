from django.shortcuts import render

# Create your views here.

def warehouses_management(request):
    return render(request, 'warehouses.html', {})
