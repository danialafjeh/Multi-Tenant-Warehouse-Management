from django import forms
from products.models import Product, Category, UnitOfMeasure



class ProductForm(forms.ModelForm):
    name = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Thermal labels 100x150",
        }),
    )

    sku = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "TL-100150",
        }),
    )

    category = forms.ModelChoiceField(
        queryset=Category.objects.none(),
        required=False,
        empty_label="Select category",
        widget=forms.Select(attrs={
            "class": "form-select",
        }),
    )

    unit = forms.ModelChoiceField(
        queryset=UnitOfMeasure.objects.none(),
        empty_label="Select unit of measure",
        widget=forms.Select(attrs={
            "class": "form-select",
        }),
    )

    reorder_level = forms.DecimalField(
        max_digits=12,
        decimal_places=3,
        min_value=0,
        initial=0,
        widget=forms.NumberInput(attrs={
            "class": "form-control",
            "placeholder": "0",
            "min": "0",
            "step": "0.001",
        }),
    )

    description = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            "class": "form-control",
            "rows": 2,
            "placeholder": "Product description",
        }),
    )

    class Meta:
        model = Product
        fields = [
            "name",
            "sku",
            "category",
            "unit",
            "reorder_level",
            "description",
        ]

    def __init__(self, *args, organization=None, **kwargs):
        super().__init__(*args, **kwargs)

        if organization is not None:
            self.fields["category"].queryset = (
                Category.objects
                .filter(organization=organization)
                .order_by("name")
            )

            self.fields["unit"].queryset = (
                UnitOfMeasure.objects
                .filter(organization=organization)
                .order_by("name")
            )



class UnitOfMeasureForm(forms.ModelForm):
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Piece",
        }),
    )

    abbreviation = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "pc",
        }),
    )

    class Meta:
        model = UnitOfMeasure
        fields = [
            "name",
            "abbreviation",
        ]