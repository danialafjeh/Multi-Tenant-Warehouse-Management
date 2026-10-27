from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout
from django.db import transaction
from .models import Membership
from django.contrib import messages
from django.db import IntegrityError
from .forms import AddMemberForm
from .services import create_member, remove_member, delete_organization

# Create your views here.

def members_management_page(request):
    if not request.user.is_authenticated:
        messages.error(request, 'Please log in to access the dashboard.')
        return redirect('home_page')
    
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



def add_member_system(request):
    if not request.user.is_authenticated:
        messages.error(request, 'Please log in to access the dashboard.')
        return redirect('home_page')
    
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



def remove_member_system(request, user_id):
    if not request.user.is_authenticated:
        messages.error(request, 'Please log in to access the dashboard.')
        return redirect('home_page')
    
    current_membership = get_object_or_404(
        Membership.objects.select_related("organization"),
        user=request.user,
    )

    if current_membership.role != "manager":
        messages.error(request,"You do not have permission to remove members.")
        return redirect('members_management_page')

    if user_id == request.user.pk:
        messages.error(request, "You cannot remove your own account.")
        return redirect("members_management_page")

    target_membership = get_object_or_404(
        Membership.objects.select_related("user"),
        user_id=user_id,
        organization=current_membership.organization,
    )

    remove_member(user=target_membership.user)

    messages.success(request, "Member removed successfully.")
    return redirect("members_management_page")



def delete_organization_page(request):
    if not request.user.is_authenticated:
        messages.error(request, 'Please log in to access the dashboard.')
        return redirect('home_page')
    
    membership = get_object_or_404(
        Membership,
        user=request.user,
        is_active=True,
    )

    if membership.role != "manager":
        messages.error(request, 'Only manager can delete the organization.')
        return redirect("members_management_page")

    return render(request, "delete_organization.html")



def delete_organization_system(request):
    if not request.user.is_authenticated:
        messages.error(request, 'Please log in to access the dashboard.')
        return redirect('home_page')
    
    if request.method == "POST":
        current_membership = get_object_or_404(
            Membership.objects.select_related("organization"),
            user=request.user,
        )

        if current_membership.role != "manager":
            messages.error(request,"You do not have permission to delete this organization.",)
            return redirect("members_management_page")

        organization_id = current_membership.organization_id

        delete_organization(organization_id=organization_id)

        logout(request)

        messages.success(request,"The organization and its associated data have been permanently deleted.")
        return redirect("home_page")
    else:
        messages.error(request, "Invalid request method.")
        return redirect("members_management_page")
    