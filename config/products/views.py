from django.shortcuts import render

# Create your views here.

def products_management(request):
    return render(request, 'products.html', {})



def categories_management(request):
    return render(request, 'categories.html', {})
