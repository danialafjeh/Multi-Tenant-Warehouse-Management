from django import forms
from products.models import Product
from warehouses.models import Warehouse



class StockInForm(forms.Form):
    product = forms.ModelChoiceField(
        queryset=Product.objects.none(),
        label="Product",
        empty_label="Select a product",
        widget=forms.Select(
            attrs={
                "class": "form-select",
            }
        ),
    )

    to_warehouse = forms.ModelChoiceField(
        queryset=Warehouse.objects.none(),
        label="To Warehouse",
        empty_label="Select a warehouse",
        widget=forms.Select(
            attrs={
                "class": "form-select",
            }
        ),
    )

    quantity = forms.DecimalField(
        label="Quantity",
        min_value=1,
        max_digits=14,
        decimal_places=1,
        widget=forms.NumberInput(
            attrs={
                "class": "form-control",
                "placeholder": "0",
                "min": "0.001",
                "step": "0.001",
            }
        ),
    )

    notes = forms.CharField(
        label="Notes (Optional)",
        required=False,
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "rows": 2,
                "placeholder": "Extra notes...",
            }
        ),
    )

    def __init__(self, *args, organization, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["product"].queryset = Product.objects.filter(
            organization=organization,
        ).order_by("name")

        self.fields["to_warehouse"].queryset = Warehouse.objects.filter(
            organization=organization,
        ).order_by("name")



class StockOutForm(forms.Form):
    product = forms.ModelChoiceField(
        queryset=Product.objects.none(),
        label="Product",
        empty_label="Select a product",
        widget=forms.Select(attrs={
            "class": "form-select",
        }),
    )

    from_warehouse = forms.ModelChoiceField(
        queryset=Warehouse.objects.none(),
        label="From Warehouse",
        empty_label="Select a warehouse",
        widget=forms.Select(attrs={
            "class": "form-select",
        }),
    )

    quantity = forms.DecimalField(
        label="Quantity",
        min_value=1,
        max_digits=14,
        decimal_places=1,
        widget=forms.NumberInput(attrs={
            "class": "form-control",
            "placeholder": "0",
            "min": "0.001",
            "step": "0.001",
        }),
    )

    notes = forms.CharField(
        required=False,
        label="Notes (Optional)",
        widget=forms.Textarea(attrs={
            "class": "form-control",
            "rows": 3,
            "placeholder": "Extra notes...",
        }),
    )

    def __init__(self, *args, organization, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["product"].queryset = (
            Product.objects
            .filter(organization=organization)
            .order_by("name")
        )

        self.fields["from_warehouse"].queryset = (
            Warehouse.objects
            .filter(organization=organization)
            .order_by("name")
        )
