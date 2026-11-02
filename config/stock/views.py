from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from organizations.models import Membership
from .forms import StockInForm, StockOutForm, TransferForm
from .services import stock_in, stock_out, transfer_stock
from .models import Inventory, StockMovement
from warehouses.models import Warehouse
from django.db.models import Q, F

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

    product_search = request.GET.get("search-1", "").strip()

    if product_search:
        inventory = inventory.filter(
            Q(product__name__icontains=product_search) |
            Q(product__sku__icontains=product_search)
        )

    warehouse_id = request.GET.get("search-2", "").strip()

    if warehouse_id:
        inventory = inventory.filter(warehouse_id=warehouse_id)

    stock_level = request.GET.get("search-3", "").strip()

    if stock_level == "in_stock":
        inventory = inventory.filter(quantity__gt=F("product__reorder_level"))
    elif stock_level == "low_stock":
        inventory = inventory.filter(quantity__gt=0, quantity__lte=F("product__reorder_level"))
    elif stock_level == "out_of_stock":
        inventory = inventory.filter(quantity=0)

    warehouses = Warehouse.objects.filter(organization=membership.organization, status='active').order_by('name')

    paginator = Paginator(inventory, 10)
    page_obj = paginator.get_page(request.GET.get("page"))

    stock_in_form = StockInForm(organization=membership.organization)
    stock_out_form = StockOutForm(organization=membership.organization)
    transfer_form = TransferForm(organization=membership.organization)

    context = {
        'inventory':page_obj,
        'page_obj':page_obj,
        'paginator':paginator,
        'warehouses':warehouses,
        'stock_in_form':stock_in_form,
        'stock_out_form':stock_out_form,
        'transfer_form':transfer_form
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

    except ValueError as e:
        messages.error(request, str(e))

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



def transfer_stock_system(request):
    if not request.user.is_authenticated:
        messages.error(
            request,
            "Please log in to access the inventory."
        )
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

    organization = membership.organization

    if membership.role not in ["manager", "staff"]:
        messages.error(request,"You do not have permission to record stock movements.")
        return redirect("inventory_management_page")

    if request.method != "POST":
        messages.error(request,"Invalid request method.")
        return redirect("inventory_management_page")

    form = TransferForm(request.POST,organization=organization)

    if not form.is_valid():
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(request, error)

        return redirect("inventory_management_page")

    product = form.cleaned_data["product"]
    from_warehouse = form.cleaned_data["from_warehouse"]
    to_warehouse = form.cleaned_data["to_warehouse"]
    quantity = form.cleaned_data["quantity"]
    notes = form.cleaned_data["notes"]

    try:
        transfer_stock(
            organization=organization,
            product=product,
            from_warehouse=from_warehouse,
            to_warehouse=to_warehouse,
            quantity=quantity,
            notes=notes,
            user=request.user,
        )

        messages.success(request,"Stock has been transferred successfully.")

    except ValueError as e:
        messages.error(request,str(e))

    except Exception:
        messages.error(request,"An unexpected error occurred while transferring stock.")

    return redirect("inventory_management_page")



def stock_movements_management_page(request):
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
        messages.error(request,"You do not have permission to access this page.")
        return redirect("home_page")

    organization = membership.organization

    stock_movements = (
        StockMovement.objects
        .select_related(
            "product_snapshot",
            "warehouse",
            "from_warehouse",
            "to_warehouse",
            "recorded_by_snapshot",
        )
        .filter(organization=organization)
        .order_by("-created_at")
    )

    date_from = request.GET.get("date_from", "").strip()
    date_to = request.GET.get("date_to", "").strip()
    movement_type = request.GET.get("movement_type", "").strip()
    warehouse_id = request.GET.get("warehouse", "").strip()
    product = request.GET.get("product", "").strip()

    if date_from:
        stock_movements = stock_movements.filter(created_at__date__gte=date_from)

    if date_to:
        stock_movements = stock_movements.filter(created_at__date__lte=date_to)

    if movement_type in {"stock_in","stock_out","transfer"}:
        stock_movements = stock_movements.filter(movement_type=movement_type)

    if warehouse_id.isdigit():
        warehouse_id = int(warehouse_id)
    
        warehouse_exists = Warehouse.objects.filter(pk=warehouse_id, organization=organization).exists()

        if warehouse_exists:
            stock_movements = stock_movements.filter(
                Q(warehouse_id=warehouse_id)
                | Q(from_warehouse_id=warehouse_id)
                | Q(to_warehouse_id=warehouse_id)
            )

    if product:
        stock_movements = stock_movements.filter(
            Q(product_snapshot__name__icontains=product)
            | Q(product_snapshot__sku__icontains=product)
        )

    paginator = Paginator(stock_movements, 10)
    page_obj = paginator.get_page(request.GET.get("page"))

    warehouses = (
        Warehouse.objects
        .filter(organization=organization, status='active')
        .order_by("name")
    )

    context = {
        "stock_movements": page_obj,
        "paginator": paginator,
        "page_obj": page_obj,
        "warehouses": warehouses,
        "filters": {
            "date_from": date_from,
            "date_to": date_to,
            "movement_type": movement_type,
            "warehouse": str(warehouse_id) if warehouse_id else "",
            "product": product,
        },
    }

    return render(request, "stock_movements.html", context)
