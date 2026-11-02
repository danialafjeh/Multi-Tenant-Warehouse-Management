from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import IntegrityError
from .forms import SignUpForm, LoginForm
from .services import register_user
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required

# Create your views here.

def home_page(request):
    return render(request, 'home.html', {})



def login_system(request):
    if request.user.is_authenticated:
        return redirect("dashboard_management_pages")

    if request.method == "POST":
        form = LoginForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()

            login(request, user)

            messages.success(
                request,
                "You have logged in successfully.",
            )

            return redirect("dashboard_management_page")

    else:
        form = LoginForm(request)

    return render(request, "login.html", {"form": form})



def signup_system(request):
    if request.user.is_authenticated:
        return redirect("dashboard_management")

    if request.method == "POST":
        form = SignUpForm(request.POST)

        if form.is_valid():
            try:
                register_user(
                    first_name=form.cleaned_data["first_name"],
                    last_name=form.cleaned_data["last_name"],
                    username=form.cleaned_data["username"],
                    email=form.cleaned_data["email"],
                    password=form.cleaned_data["password1"],
                    organization_name=form.cleaned_data["organization_name"],
                )
            except IntegrityError:
                messages.error(
                    request,
                    "We couldn't create your account. Please check your information and try again.",
                )
                return redirect('signup_system')
            else:
                messages.success(
                    request,
                    "Your account has been created successfully. "
                    "You can now log in.",
                )
                return redirect("login_system")
    else:
        form = SignUpForm()

    return render(
        request,
        "signup.html",
        {"form": form}
    )



def logout_system(request):
    if not request.user.is_authenticated:
        messages.error(request, 'Please log in to access the dashboard.')
        return redirect('home_page')

    if request.method == "POST":
        logout(request)
        messages.success(request, "You have logged out successfully.")
        return redirect("home_page")

    return redirect("dashboard_management")
