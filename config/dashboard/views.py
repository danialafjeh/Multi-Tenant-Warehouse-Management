from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, F
from django.db.models.functions import Coalesce
from django.views.decorators.http import require_GET
from decimal import Decimal
from organizations.models import Membership
from warehouses.models import Warehouse
from products.models import Product
from stock.models import Inventory , StockMovement

# Create your views here.

def dashboard_management_page(request):
    if not request.user.is_authenticated:
        messages.error(request,"You must be logged in to access the dashboard.")
        return redirect("home_page")

    membership = (
        Membership.objects
        .select_related("organization")
        .filter(user=request.user)
        .first()
    )

    if not membership:
        messages.error(request,"You are not a member of any organization.")
        return redirect("home_page")

    warehouses = Warehouse.objects.filter(
        organization=membership.organization
    )

    warehouses_count = warehouses.count()

    products = Product.objects.filter(organization=membership.organization)

    products_count = products.count()

    inventory = Inventory.objects.filter(warehouse__organization=membership.organization)

    total_units = inventory.aggregate(
        total=Coalesce(Sum("quantity"),Decimal("0.0"))
    )["total"]

    low_stock_inventory = (
        inventory
        .filter(
            quantity__lte=F("product__reorder_level")
        )
        .select_related(
            "product",
            "warehouse"
        )
        .order_by(
            "quantity",
            "product__name"
        )
    )

    low_stock_count = low_stock_inventory.count()

    recent_movements = (
        StockMovement.objects
        .filter(
            organization=membership.organization
        )
        .select_related(
            "product_snapshot",
            "warehouse",
            "from_warehouse",
            "to_warehouse",
            "recorded_by_snapshot"
        )
        .order_by("-created_at")[:5]
    )

    context = {
        "warehouses_count": warehouses_count,
        "products_count": products_count,
        "total_units": total_units,
        "low_stock_count": low_stock_count,
        "recent_movements": recent_movements,
        "low_stock_inventory": low_stock_inventory,
    }

    return render(request, "dashboard.html", context)
