from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Membership
from django.contrib import messages
from django.db import IntegrityError
from .forms import AddMemberForm
from .services import create_member

# Create your views here.

def members_management_page(request):
    membership = (
        Membership.objects.select_related("organization").get(user=request.user)
    )

    members = (
        Membership.objects
        .filter(organization=membership.organization)
        .select_related("user", "user__snapshot")
        .order_by("user__first_name", "user__last_name", "user__username")
    )

    form = AddMemberForm()

    context = {
        'membership':membership,
        "members": members,
        "form":form
    }
    
    return render(request, "members.html", context)



@login_required
def add_member_system(request):
    membership = (
        Membership.objects
        .select_related("organization")
        .filter(user=request.user)
        .first()
    )

    if membership is None:
        messages.error(request,"You do not have permission to perform this action.")
        return redirect("home_page")
    elif  membership.role != "manager":
        messages.error(request,"Only manager can add members.")
        return redirect("members_management_page")

    if request.method == "POST":
        form = AddMemberForm(request.POST)

        if form.is_valid():
            try:
                create_member(
                    first_name=form.cleaned_data["first_name"],
                    last_name=form.cleaned_data["last_name"],
                    username=form.cleaned_data["username"],
                    email=form.cleaned_data["email"],
                    password=form.cleaned_data["password1"],
                    role=form.cleaned_data["role"],
                    organization=membership.organization,
                )

            except IntegrityError:
                messages.error(request,"Error, Unable to add the member.")
                return redirect('members_management_page')

            else:
                messages.success(request,"Member added successfully.")
                return redirect('members_management_page')
        else:
            for field, errors in form.errors.items():
               for error in errors:
                   messages.error(request, error)

            return redirect("members_management_page")

    else:
        messages.error(request,"Invalid request method.")
        return redirect("home_page")
        