from django.shortcuts import render

# Create your views here.

def inventory_management(request):
    return render(request, 'inventory.html', {})



def stock_movements_management(request):
    return render(request, 'stock_movements.html', {})
