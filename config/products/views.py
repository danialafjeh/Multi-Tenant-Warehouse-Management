from django.shortcuts import render

# Create your views here.

def products_management(request):
    return render(request, 'products.html', {})



def categories_management(request):
    return render(request, 'categories.html', {})



def units_of_measure_management(request):
    return render(request, 'unitsofmeasure.html', {})
