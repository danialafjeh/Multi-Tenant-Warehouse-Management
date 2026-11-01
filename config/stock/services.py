from django.db import IntegrityError, transaction
from products.models import ProductSnapshot
from accounts.models import UserSnapshot
from warehouses.models import Warehouse
from .models import Inventory, StockMovement
from django.utils import timezone



def stock_in(*, organization, product, warehouse, quantity, notes, user):
    with transaction.atomic():

        warehouse = (
            Warehouse.objects
           .select_for_update()
           .get(
                pk=warehouse.pk,
                organization=organization,
            )
        )

        if warehouse.status != "active":
            raise ValueError(
                "Stock operations are not allowed in an inactive warehouse."
            )

        inventory = (
            Inventory.objects
            .select_for_update()
            .filter(
                organization=organization,
                warehouse=warehouse,
                product=product,
            )
            .first()
        )

        

        if inventory is None:
            try:
                with transaction.atomic():
                    inventory = Inventory.objects.create(
                        organization=organization,
                        warehouse=warehouse,
                        product=product,
                        quantity=quantity,
                    )

            except IntegrityError:
                inventory = (
                    Inventory.objects
                    .select_for_update()
                    .get(
                        organization=organization,
                        warehouse=warehouse,
                        product=product,
                    )
                )

                inventory.quantity += quantity

                inventory.save(
                    update_fields=[
                        "quantity",
                        "updated_at",
                    ],
                )

        else:
            inventory.quantity += quantity

            inventory.save(
                update_fields=[
                    "quantity",
                    "updated_at",
                ],
            )

        product_snapshot = ProductSnapshot.objects.create(
            organization=organization,
            product=product,
            name=product.name,
            sku=product.sku,
            category_name=(product.category.name if product.category else ""),
            unit_name=product.unit.name,
            unit_abbreviation=product.unit.abbreviation,
            reorder_level=product.reorder_level,
            description=product.description,
        )

        user_snapshot, created = (
            UserSnapshot.objects.get_or_create(
                user=user,
                defaults={
                    "username": user.username,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "email": user.email,
                },
            )
        )

        stock_movement = StockMovement.objects.create(
            organization=organization,
            product_snapshot=product_snapshot,
            movement_type="stock_in",
            warehouse=warehouse,
            quantity=quantity,
            notes=notes,
            recorded_by=user,
            recorded_by_snapshot=user_snapshot,
        )

        return inventory, stock_movement



@transaction.atomic
def stock_out(*, organization, product, warehouse, quantity, notes, user):
    warehouse = (
        Warehouse.objects
        .select_for_update()
        .get(
            pk=warehouse.pk,
            organization=organization,
        )
    )
    
    if warehouse.status != "active":
        raise ValueError(
            "Stock operations are not allowed in an inactive warehouse."
        )
    
    inventory = (
        Inventory.objects
        .select_for_update()
        .filter(
            organization=organization,
            product=product,
            warehouse=warehouse,
        )
        .first()
    )

    if inventory is None:
        raise ValueError(
            "No inventory record exists for this product in the selected warehouse."
        )

    if inventory.quantity < quantity:
        raise ValueError(
            "Insufficient stock. The available quantity is not enough for this operation."
        )

    inventory.quantity -= quantity

    inventory.save(
        update_fields=[
            "quantity",
            "updated_at",
        ]
    )

    product_snapshot = ProductSnapshot.objects.create(
        organization=organization,
        product=product,
        name=product.name,
        sku=product.sku,
        category_name=(product.category.name if product.category else ""
        )
    )

    user_snapshot, created = UserSnapshot.objects.get_or_create(
        user=user,
        defaults={
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
        },
    )

    stock_movement = StockMovement.objects.create(
        organization=organization,
        product_snapshot=product_snapshot,
        movement_type="stock_out",
        warehouse=None,
        from_warehouse=warehouse,
        to_warehouse=None,
        quantity=quantity,
        notes=notes,
        recorded_by=user,
        recorded_by_snapshot=user_snapshot,
    )

    return inventory, stock_movement



@transaction.atomic
def transfer_stock(*, organization, product, from_warehouse, to_warehouse, quantity, notes, user):
    if from_warehouse == to_warehouse:
        raise ValueError(
            "The source and destination warehouses must be different."
        )

    if quantity <= 0:
        raise ValueError(
            "Transfer quantity must be greater than zero."
        )

    if (
        from_warehouse.organization_id != organization.id
        or to_warehouse.organization_id != organization.id
        or product.organization_id != organization.id
    ):
        raise ValueError(
            "The selected product or warehouses do not belong to your organization."
        )

    if (
        from_warehouse.status != "active"
        or to_warehouse.status != "active"
    ):
        raise ValueError(
            "Both warehouses must be active to perform a transfer."
        )

    warehouse_ids = sorted(
        [from_warehouse.id, to_warehouse.id]
    )

    locked_inventory = list(
        Inventory.objects
        .select_for_update()
        .filter(
            organization=organization,
            product=product,
            warehouse_id__in=warehouse_ids,
        )
        .order_by("warehouse_id")
    )

    inventory_by_warehouse = {
        item.warehouse_id: item
        for item in locked_inventory
    }

    source_inventory = inventory_by_warehouse.get(from_warehouse.id)

    if source_inventory is None:
        raise ValueError(
            "No inventory record exists for this product in the source warehouse."
        )

    if source_inventory.quantity < quantity:
        raise ValueError(
            "Insufficient stock. The available quantity is not enough for this transfer."
        )

    destination_inventory = inventory_by_warehouse.get(to_warehouse.id)

    source_inventory.quantity -= quantity

    source_inventory.save(
        update_fields=[
            "quantity",
            "updated_at",
        ]
    )

    if destination_inventory is None:
        try:
            with transaction.atomic():
                destination_inventory = Inventory.objects.create(
                    organization=organization,
                    product=product,
                    warehouse=to_warehouse,
                    quantity=quantity,
                )

        except IntegrityError:
            destination_inventory = (
                Inventory.objects
                .select_for_update()
                .get(
                    organization=organization,
                    product=product,
                    warehouse=to_warehouse,
                )
            )

            destination_inventory.quantity += quantity

            destination_inventory.save(
                update_fields=[
                    "quantity",
                    "updated_at",
                ]
            )

    else:
        destination_inventory.quantity += quantity

        destination_inventory.save(
            update_fields=[
                "quantity",
                "updated_at",
            ]
        )

    product_snapshot = ProductSnapshot.objects.create(
        organization=organization,
        product=product,
        name=product.name,
        sku=product.sku,
        category_name=(
            product.category.name
            if product.category
            else ""
        ),
    )

    user_snapshot, created = UserSnapshot.objects.get_or_create(
        user=user,
        defaults={
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
        },
    )

    stock_movement = StockMovement.objects.create(
        organization=organization,
        product_snapshot=product_snapshot,
        movement_type="transfer",
        warehouse=None,
        from_warehouse=from_warehouse,
        to_warehouse=to_warehouse,
        quantity=quantity,
        notes=notes,
        recorded_by=user,
        recorded_by_snapshot=user_snapshot,
    )

    return (
        source_inventory,
        destination_inventory,
        stock_movement,
    )