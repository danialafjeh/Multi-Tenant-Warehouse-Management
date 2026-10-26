from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User



class SignUpForm(UserCreationForm):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(
            attrs={
                "id": "usernamename",
                "class": "form-control",
                "placeholder": "danialafjeh",
                "autocomplete": "username",
            }
        ),
        label="Username",
    )
     
    first_name = forms.CharField(
        max_length=150,
        widget=forms.TextInput(
            attrs={
                "id": "first_name",
                "class": "form-control",
                "placeholder": "Danial",
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
                "placeholder": "Afjeh",
                "autocomplete": "family-name",
            }
        ),
        label="Last name",
    )

    organization_name = forms.CharField(
        max_length=255,
        widget=forms.TextInput(
            attrs={
                "id": "org",
                "class": "form-control",
                "placeholder": "Afjeh Co.",
            }
        ),
        label="Organization name",
    )

    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "id": "email",
                "class": "form-control",
                "placeholder": "you@company.com",
                "autocomplete": "email",
            }
        ),
        label="Work email",
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
                "placeholder": "At least 8 characters",
                "autocomplete": "new-password",
            }
        ),
        label="Confirm password",
    )

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "username",
            "email",
            "password1",
            "password2",
        )

    def clean_username(self):
        username = self.cleaned_data["username"]

        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(
                "This username is already taken."
            )

        return username



class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "id": "username",
                "class": "form-control",
                "placeholder": "Your userame",
                "autocomplete": "username",
            }
        ),
        label="Username",
    )

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "id": "password",
                "class": "form-control",
                "placeholder": "At least 8 characters",
                "autocomplete": "current-password",
            }
        ),
        label="Password",
    )
    