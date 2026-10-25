from django.contrib import admin
from .models import Category, UnitOfMeasure, Product

# Register your models here.

admin.site.register(Category)
admin.site.register(UnitOfMeasure)
admin.site.register(Product)
