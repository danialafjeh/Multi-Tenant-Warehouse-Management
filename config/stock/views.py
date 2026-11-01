from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from organizations.models import Membership
from .forms import StockInForm, StockOutForm
from .services import stock_in, stock_out
from .models import Inventory, StockMovement

# Create your views here.

def inventory_management_page(request):
    if not request.user.is_authenticated:
        messages.error(request, "Please log in to access the dashboard.")
        return redirect("home_page")
         
    membership = (
        Membership.objects
        .select_related("organization")
        .filter(user=request.user)
        .first()
    )
    
    if membership is None:
        messages.error(request, "You do not have permission to access this page.")
        return redirect("home_page")

    inventory = ( 
        Inventory.objects
        .select_related('product','warehouse')
        .filter(organization=membership.organization)
        .order_by('-updated_at') 
    )

    stock_in_form = StockInForm(organization=membership.organization)
    stock_out_form = StockOutForm(organization=membership.organization)

    context = {
        'inventory':inventory,
        'stock_in_form':stock_in_form,
        'stock_out_form':stock_out_form
    }

    return render(request, 'inventory.html', context)



def stock_in_system(request):
    if not request.user.is_authenticated:
        messages.error(request,"Please log in to access the dashboard.")
        return redirect("home_page")

    membership = (
        Membership.objects
        .select_related("organization")
        .filter(user=request.user)
        .first()
    )

    if membership is None:
        messages.error(request,"You are not a member of any organization.")
        return redirect("home_page")

    if membership.role not in ['manager','staff']:
        messages.error(request,"You do not have permission to record stock movements.")
        return redirect("inventory_management_page")

    if request.method != "POST":
        messages.error(request,"Invalid request method.")
        return redirect("inventory_management_page")

    form = StockInForm(request.POST,organization=membership.organization)

    if not form.is_valid():
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(request, error)

        return redirect("inventory_management_page")

    product = form.cleaned_data["product"]
    warehouse = form.cleaned_data["to_warehouse"]
    quantity = form.cleaned_data["quantity"]
    notes = form.cleaned_data["notes"]

    try:
        stock_in(
            organization=membership.organization,
            product=product,
            warehouse=warehouse,
            quantity=quantity,
            notes=notes,
            user=request.user,
        )

        messages.success(request,"Stock has been added successfully.")

    except Exception:
        messages.error(request,"An unexpected error occurred while adding stock.")

    return redirect("inventory_management_page")



def stock_out_system(request):
    if not request.user.is_authenticated:
        messages.error(request,"Please log in to access the dashboard.")
        return redirect("home_page")

    membership = (
        Membership.objects
        .select_related("organization")
        .filter(user=request.user)
        .first()
    )

    if membership is None:
        messages.error(request,"You are not a member of any organization.")
        return redirect("home_page")

    if membership.role not in ["manager", "staff"]:
        messages.error(request,"You do not have permission to record stock movements.")
        return redirect("inventory_management_page")

    if request.method != "POST":
        messages.error(request,"Invalid request method.")
        return redirect("inventory_management_page")

    form = StockOutForm(request.POST, organization=membership.organization)

    if not form.is_valid():
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(request, error)

        return redirect("inventory_management_page")

    product = form.cleaned_data["product"]
    warehouse = form.cleaned_data["from_warehouse"]
    quantity = form.cleaned_data["quantity"]
    notes = form.cleaned_data["notes"]

    try:
        stock_out(
            organization=membership.organization,
            product=product,
            warehouse=warehouse,
            quantity=quantity,
            notes=notes,
            user=request.user,
        )

        messages.success(request,"Stock has been removed successfully.")

    except ValueError as e:
        messages.error(request, str(e))

    except Exception:
        messages.error(request,"An unexpected error occurred while removing stock.")

    return redirect("inventory_management_page")



def stock_movements_management(request):
    return render(request, 'stock_movements.html', {})
