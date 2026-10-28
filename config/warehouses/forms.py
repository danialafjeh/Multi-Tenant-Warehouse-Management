from django import forms
from .models import Warehouse



class WarehouseForm(forms.ModelForm):
    name = forms.CharField(
        max_length=150,
        widget=forms.TextInput(
            attrs={
                "id": "name",
                "class": "form-control",
                "placeholder": "Main warehouse",
            }
        ),
        label="Warehouse name",
    )

    code = forms.CharField(
        max_length=50,
        widget=forms.TextInput(
            attrs={
                "id": "code",
                "class": "form-control",
                "placeholder": "WH-05",
                "autocomplete": "off",
            }
        ),
        label="Warehouse code",
        help_text="A unique code for each warehouse within your organization.",
    )

    status = forms.ChoiceField(
        choices=Warehouse.STATUS_CHOICES,
        widget=forms.Select(
            attrs={
                "id": "status",
                "class": "form-select",
            }
        ),
        label="Status",
    )

    location = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(
            attrs={
                "id": "location",
                "class": "form-control",
                "placeholder": "City, street",
            }
        ),
        label="Location",
    )

    notes = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                "id": "notes",
                "class": "form-control",
                "rows": 2,
                "placeholder": "Opening hours, gate access, contact person",
            }
        ),
        label="Notes",
    )

    class Meta:
        model = Warehouse
        fields = (
            "name",
            "code",
            "status",
            "location",
            "notes",
        )
