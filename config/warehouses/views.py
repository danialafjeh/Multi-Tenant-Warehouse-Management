from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from organizations.models import Membership
from .models import Warehouse
from django.db import IntegrityError
from .forms import WarehouseForm

# Create your views here.

def warehouses_management_page(request):
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
    
    search_query = request.GET.get("search", "").strip()

    warehouses = (
        Warehouse.objects
        .filter(organization=membership.organization)
        .order_by("name")
    )

    if search_query:
        warehouses = warehouses.filter(Q(name__icontains=search_query) | Q(code__iexact=search_query))
 
    paginator = Paginator(warehouses, 3)
    page_obj = paginator.get_page(request.GET.get("page"))

    form = WarehouseForm()

    context = {
        "membership": membership,
        "warehouses": page_obj,
        "page_obj": page_obj,
        "paginator": paginator,
        "form": form,
        "search_query": search_query
    }

    return render(request, "warehouses.html", context)



def add_warehouse_system(request):
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
        messages.error(request,"You do not have permission to perform this action.",)
        return redirect("home_page")

    elif membership.role != "manager":
        messages.error(request,"Only manager can add warehouses.")
        return redirect("warehouses_management_page")

    if request.method == "POST":
        form = WarehouseForm(request.POST)

        if form.is_valid():
            warehouse = form.save(commit=False)
            warehouse.organization = membership.organization

            try:
                warehouse.save()

            except IntegrityError:
                messages.error(
                    request,
                    "Error, unable to create the warehouse. "
                    "Please check the warehouse code.",
                )
                return redirect("warehouses_management_page")

            else:
                messages.success(request,"Warehouse added successfully.")
                return redirect("warehouses_management_page")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, error)

            return redirect("warehouses_management_page")
    else:
        messages.error(request,"Invalid request method.")
        return redirect("home_page")



def edit_warehouse_system(request, warehouse_id):
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
        messages.error(request,"You do not have permission to perform this action.")
        return redirect("home_page")

    elif membership.role != "manager":
        messages.error(request,"Only manager can edit warehouses.")
        return redirect("warehouses_management_page")

    warehouse = get_object_or_404(
        Warehouse,
        id=warehouse_id,
        organization=membership.organization,
    )

    if request.method == "POST":
        form = WarehouseForm(request.POST, instance=warehouse)

        if form.is_valid():
            try:
                form.save()

            except IntegrityError:
                messages.error(
                    request,
                    "Error, unable to update the warehouse. "
                    "Please check the warehouse code.",
                )
                return redirect("warehouses_management_page")

            else:
                messages.success(request,"Warehouse updated successfully.")
                return redirect("warehouses_management_page")

        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, error)

            return redirect("warehouses_management_page")

    else:
        messages.error(request,"Invalid request method.")
        return redirect("home_page")
