from django.db import models
from django.contrib.auth.models import User
from organizations.models import Organization
from warehouses.models import Warehouse
from products.models import Product
from accounts.models import UserSnapshot

# Create your models here.

class Inventory(models.Model):
    organization = models.ForeignKey(
        Organization,
        on_delete=models.PROTECT,
        related_name="stock_levels",
    )
    warehouse = models.ForeignKey(
        Warehouse,
        on_delete=models.PROTECT,
        related_name="stock_levels",
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        related_name="stock_levels",
    )
    quantity = models.DecimalField(
        max_digits=14,
        decimal_places=1,
        default=0,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["warehouse__name", "product__name"]
        constraints = [
            models.UniqueConstraint(
                fields=["warehouse", "product"],
                name="unique_product_stock_per_warehouse",
            ),
            models.CheckConstraint(
                condition=models.Q(quantity__gte=0),
                name="stock_quantity_non_negative",
            ),
        ]
        verbose_name = "Inventory Level"
        verbose_name_plural = "Inventory Levels"

    def __str__(self):
        return (
            f"{self.product.name} - "
            f"{self.warehouse.name}: {self.quantity}"
        )

    @property
    def stock_status(self):
        if self.quantity == 0:
            return "out_of_stock"

        if self.quantity <= self.product.reorder_level:
            return "low_stock"

        return "in_stock"



class StockMovement(models.Model):
    MOVEMENT_TYPES = [
        ("stock_in", "Stock In"),
        ("stock_out", "Stock Out"),
        ("transfer", "Transfer"),
    ]

    organization = models.ForeignKey(
        Organization,
        on_delete=models.PROTECT,
        related_name="stock_movements",
    )
    product_snapshot = models.ForeignKey(
       "products.ProductSnapshot",
       on_delete=models.PROTECT,
       related_name="stock_movements"
    )
    movement_type = models.CharField(
        max_length=20,
        choices=MOVEMENT_TYPES,
    )
    warehouse = models.ForeignKey(
        Warehouse,
        on_delete=models.PROTECT,
        related_name="stock_movements",
        null=True,
        blank=True,
    )
    from_warehouse = models.ForeignKey(
        Warehouse,
        on_delete=models.PROTECT,
        related_name="outgoing_transfers",
        null=True,
        blank=True,
    )
    to_warehouse = models.ForeignKey(
        Warehouse,
        on_delete=models.PROTECT,
        related_name="incoming_transfers",
        null=True,
        blank=True,
    )
    quantity = models.DecimalField(
        max_digits=14,
        decimal_places=1,
    )
    notes = models.TextField(
        blank=True,
    )
    recorded_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name="recorded_stock_movements",
        null=True,
        blank=True,
    )
    recorded_by_snapshot = models.ForeignKey(
        UserSnapshot,
        on_delete=models.PROTECT,
        related_name="stock_movements",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            models.CheckConstraint(
                condition=models.Q(quantity__gt=0),
                name="stock_movement_quantity_positive",
            ),
            models.CheckConstraint(
                condition=(
                    models.Q(
                        movement_type="stock_in",
                        warehouse__isnull=False,
                        from_warehouse__isnull=True,
                        to_warehouse__isnull=True,
                    )
                    |
                    models.Q(
                        movement_type="stock_out",
                        warehouse__isnull=False,
                        from_warehouse__isnull=True,
                        to_warehouse__isnull=True,
                    )
                    |
                    models.Q(
                        movement_type="transfer",
                        warehouse__isnull=True,
                        from_warehouse__isnull=False,
                        to_warehouse__isnull=False,
                    )
                ),
                name="stock_movement_warehouse_fields_valid",
            ),
            models.CheckConstraint(
                condition=(
                    ~models.Q(movement_type="transfer")
                    |
                    ~models.Q(from_warehouse=models.F("to_warehouse"))
                ),
                name="stock_transfer_warehouses_different",
            ),
        ]
        verbose_name = "Stock Movement"
        verbose_name_plural = "Stock Movements"

    def __str__(self):
        return (
            f"{self.get_movement_type_display()} - {self.organization}"
        )