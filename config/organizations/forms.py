from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User



class AddMemberForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=150,
        widget=forms.TextInput(
            attrs={
                "id": "first_name",
                "class": "form-control",
                "placeholder": "Member's first name",
                "autocomplete": "given-name",
            }
        ),
        label="First name",
    )

    last_name = forms.CharField(
        max_length=150,
        widget=forms.TextInput(
            attrs={
                "id": "last_name",
                "class": "form-control",
                "placeholder": "Member's last name",
                "autocomplete": "family-name",
            }
        ),
        label="Last name",
    )

    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(
            attrs={
                "id": "username",
                "class": "form-control",
                "placeholder": "Member's username",
                "autocomplete": "off",
            }
        ),
        label="Username",
    )

    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "id": "email",
                "class": "form-control",
                "placeholder": "member@example.com",
                "autocomplete": "email",
            }
        ),
        label="Work email",
    )

    role = forms.ChoiceField(
        choices=[
            ("staff", "Warehouse staff"),
            ("viewer", "Viewer"),
        ],
        widget=forms.Select(
            attrs={
                "id": "role",
                "class": "form-select",
            }
        ),
        label="Role",
        help_text="Staff can record stock movements. Viewers can only look.",
    )

    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "id": "password",
                "class": "form-control",
                "placeholder": "At least 8 characters",
                "autocomplete": "new-password",
            }
        ),
        label="Password",
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "id": "password2",
                "class": "form-control",
                "placeholder": "Confirm password",
                "autocomplete": "new-password",
            }
        ),
        label="Confirm password",
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = (
            "first_name",
            "last_name",
            "username",
            "email",
        )



class CreateAPIKeyForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        label="Name",
        widget=forms.TextInput(attrs={
            "id": "api-key-name",
            "class": "form-control",
            "placeholder": "Enter a name for your API key",
            "autocomplete": "off",
        })
    )
