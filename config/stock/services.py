from django.db import IntegrityError, transaction
from products.models import ProductSnapshot
from accounts.models import UserSnapshot
from .models import Inventory, StockMovement
from django.utils import timezone



def stock_in(*, organization, product, warehouse, quantity, notes, user):
    with transaction.atomic():

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
