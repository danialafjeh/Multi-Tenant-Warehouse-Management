from django.db import models
from organizations.models import Organization

# Create your models here.

class Category(models.Model):
    organization = models.ForeignKey(
        Organization,
        on_delete=models.PROTECT,
        related_name="categories",
    )
    name = models.CharField(
        max_length=100,
    )
    description = models.TextField(
        blank=True,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["name"]
        constraints = [
            models.UniqueConstraint(
                fields=["organization", "name"],
                name="unique_category_per_organization",
            ),
        ]
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name



class UnitOfMeasure(models.Model):
    organization = models.ForeignKey(
        Organization,
        on_delete=models.PROTECT,
        related_name="units_of_measure",
    )
    name = models.CharField(
        max_length=100,
    )
    abbreviation = models.CharField(
        max_length=20,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["name"]
        constraints = [
            models.UniqueConstraint(
                fields=["organization", "name"],
                name="unique_unit_name_per_organization",
            ),
            models.UniqueConstraint(
                fields=["organization", "abbreviation"],
                name="unique_unit_abbreviation_per_organization",
            ),
        ]
        verbose_name = "Unit of Measure"
        verbose_name_plural = "Units of Measure"

    def __str__(self):
        return f"{self.name} ({self.abbreviation})"



class Product(models.Model):
    organization = models.ForeignKey(
        Organization,
        on_delete=models.PROTECT,
        related_name="products",
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="products",
        null=True,
        blank=True,
    )
    unit = models.ForeignKey(
        UnitOfMeasure,
        on_delete=models.PROTECT,
        related_name="products",
    )
    name = models.CharField(
        max_length=200,
    )
    sku = models.CharField(
        max_length=100,
    )
    reorder_level = models.DecimalField(
        max_digits=12,
        decimal_places=1,
        default=0,
    )
    description = models.TextField(
        blank=True,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["name"]
        constraints = [
            models.UniqueConstraint(
                fields=["organization", "sku"],
                name="unique_product_sku_per_organization",
            ),
            models.CheckConstraint(
                condition=models.Q(reorder_level__gte=0),
                name="product_reorder_level_non_negative",
            ),
        ]
        verbose_name = "Product"
        verbose_name_plural = "Products"

    def __str__(self):
        return f"{self.name} ({self.sku})"



class ProductSnapshot(models.Model):
    organization = models.ForeignKey(
        Organization,
        on_delete=models.PROTECT,
        related_name="product_snapshots"
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="snapshots"
    )
    name = models.CharField(max_length=200)
    sku = models.CharField(max_length=100)
    category_name = models.CharField(max_length=150, blank=True)
    unit_name = models.CharField(max_length=100)
    unit_abbreviation = models.CharField(max_length=20)
    reorder_level = models.DecimalField(max_digits=12, decimal_places=1, default=0)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["organization", "sku"])
        ]

    def __str__(self):
        return f"{self.name} ({self.sku})"