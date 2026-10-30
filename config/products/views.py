from django.shortcuts import render, redirect
from django.contrib import messages
from organizations.models import Membership
from stock.models import Inventory
from .models import Category, UnitOfMeasure, Product
from .forms import ProductForm, UnitOfMeasureForm
from django.db import IntegrityError
from django.db.models.deletion import ProtectedError
from django.db import transaction


# Create your views here.

def products_management_page(request):
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

    products = Product.objects.filter(organization=membership.organization).order_by('name')
    
    form = ProductForm(organization=membership.organization)

    context = {
        'form':form,
        'products':products
    }

    return render(request, 'products.html', context)



def categories_management(request):
    return render(request, 'categories.html', {})



def units_of_measure_management_page(request):
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
    
    if membership.role not in ['manager','staff']:
        messages.error(request, "Only manager and staff can add units of measure.")
        return redirect("products_management_page")

    units_of_measure = (
        UnitOfMeasure.objects
        .filter(organization=membership.organization)
        .order_by('name')
    )

    form = UnitOfMeasureForm()

    context = {
        'form':form,
        'units':units_of_measure
    }

    return render(request, 'unitsofmeasure.html', context)



def add_product_system(request):
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

    if membership.role not in ['manager','staff']:
        messages.error(request, "Only manager and staff can add products.")
        return redirect("products_management_page")

    if request.method == "POST":
        form = ProductForm(
            request.POST,
            organization=membership.organization
        )

        if form.is_valid():
            product = form.save(commit=False)
            product.organization = membership.organization

            try:
                product.save()

            except IntegrityError:
                messages.error(
                    request,
                    "Error, unable to create the product."
                    "Please check if it's already exists."
                )
                return redirect("products_management_page")

            messages.success(request, "Product added successfully.")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, error)

        return redirect("products_management_page")
    else:
        messages.error(request,'Invalid request method.')
        return redirect('home_page')



def edit_product_system(request, pk):
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

    if membership.role not in ["manager", "staff"]:
        messages.error(request, "You do not have permission to edit products.")
        return redirect("products_management_page")

    if request.method != "POST":
        messages.error(request, "Invalid request method.")
        return redirect("home_page")

    product = (
        Product.objects
        .filter(pk=pk, organization=membership.organization)
        .first()
    )

    if product is None:
        messages.error(request, "Product not found.")
        return redirect("products_management_page")

    form = ProductForm(request.POST, instance=product, organization=membership.organization)

    if form.is_valid():
        try:
            form.save()
        
        except IntegrityError:
            messages.error(
                request,
                "Error, unable to update the product."
                "Please check if it's already exists."
            )
            return redirect("products_management_page")

        messages.success(request, "Product updated successfully.")
    else:
        for errors in form.errors.values():
            for error in errors:
                messages.error(request, error)

    return redirect("products_management_page")



def delete_product_system(request, pk):
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

    if membership.role not in ["manager", "staff"]:
        messages.error(request, "You do not have permission to delete products.")
        return redirect("products_management_page")

    if request.method != "POST":
        messages.error(request, "Invalid request method.")
        return redirect("home_page")

    try:
        with transaction.atomic():
            product = (
                Product.objects
                .select_for_update()
                .filter(
                    pk=pk,
                    organization=membership.organization
                )
                .first()
            )

            if product is None:
                messages.error(request, "Product not found.")
                return redirect("products_management_page")

            stock_levels = (
                Inventory.objects
                .select_for_update()
                .filter(
                    organization=membership.organization,
                    product=product
                )
            )

            if stock_levels.filter(quantity__gt=0).exists():
                messages.error(
                    request,
                    "This product cannot be deleted because it has stock in one or more warehouses."
                )
                return redirect("products_management_page")

            stock_levels.delete()
            product.delete()

    except ProtectedError:
        messages.error(
            request,
            "Unable to delete this product because it is still referenced by other records."
        )
        return redirect("products_management_page")

    messages.success(request, "Product deleted successfully.")
    return redirect("products_management_page")



def add_unit_of_measure_system(request):
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
        messages.error(request,"You do not have permission to access this page.")
        return redirect("home_page")

    if membership.role not in ["manager", "staff"]:
        messages.error(request,"Only manager and staff can add units of measure.")
        return redirect("units_of_measure_management_page")

    if request.method != "POST":
        messages.error(request, "Invalid request method.")
        return redirect("home_page")

    form = UnitOfMeasureForm(request.POST)

    if form.is_valid():
        unit = form.save(commit=False)
        unit.organization = membership.organization

        try:
            unit.save()

        except IntegrityError:
            messages.error(
                request,
                "Error, unable to create the unit of measure. "
                "Please check if it's already exists.",
            )
            return redirect("units_of_measure_management_page")

        messages.success(request,"Unit of measure added successfully.")
    else:
        for errors in form.errors.values():
            for error in errors:
                messages.error(request, error)

    return redirect("units_of_measure_management_page")



def edit_unit_of_measure_system(request, pk):
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

    if membership.role not in ["manager", "staff"]:
        messages.error(request, "You do not have permission to edit units of measure.")
        return redirect("units_of_measure_management_page")

    if request.method != "POST":
        messages.error(request, "Invalid request method.")
        return redirect("home_page")

    unit = (
        UnitOfMeasure.objects
        .filter(
            pk=pk,
            organization=membership.organization
        )
        .first()
    )

    if unit is None:
        messages.error(request, "Unit of measure not found.")
        return redirect("units_of_measure_management_page")

    form = UnitOfMeasureForm(request.POST,instance=unit)

    if form.is_valid():
        try:
            form.save()
        
        except IntegrityError:
            messages.error(
                request,
                "Error, unable to update the unit of measure. "
                "Please check if it's already exists.",
            )
            return redirect("units_of_measure_management_page")
        
        messages.success(request, "Unit of measure updated successfully.")
    else:
        for errors in form.errors.values():
            for error in errors:
                messages.error(request, error)

    return redirect("units_of_measure_management_page")



def delete_unit_of_measure_system(request, pk):
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

    if membership.role not in ["manager", "staff"]:
        messages.error(request, "You do not have permission to delete units of measure.")
        return redirect("units_of_measure_management_page")

    if request.method != "POST":
        messages.error(request, "Invalid request method.")
        return redirect("home_page")

    unit = (
        UnitOfMeasure.objects
        .filter(
            pk=pk,
            organization=membership.organization
        )
        .first()
    )

    if unit is None:
        messages.error(request, "Unit of measure not found.")
        return redirect("units_of_measure_management_page")

    has_products = Product.objects.filter(
        organization=membership.organization,
        unit=unit
    ).exists()

    if has_products:
        messages.error(
            request,
            "A product is using this unit of measure. Please change the product's unit of measure and try again."
        )
        return redirect("units_of_measure_management_page")

    try:
        unit.delete()

    except ProtectedError:
        messages.error(
            request,
            "A product is using this unit of measure. Please change the product's unit of measure and try again."
        )

    messages.success(request, "Unit of measure deleted successfully.")
    return redirect("units_of_measure_management_page")
