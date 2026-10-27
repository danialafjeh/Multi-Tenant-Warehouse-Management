from django.contrib.auth.models import User
from django.db import transaction
from accounts.models import UserSnapshot
from .models import Membership



@transaction.atomic
def create_member(*, first_name, last_name, username, email, password, role, organization):
    user = User.objects.create_user(
        username=username,
        email=email,
        password=password,
        first_name=first_name,
        last_name=last_name,
    )

    UserSnapshot.objects.create(
        user=user,
        first_name=first_name,
        last_name=last_name,
        username=username,
        email=email,
    )

    membership = Membership.objects.create(
        user=user,
        organization=organization,
        role=role,
    )

    return membership



@transaction.atomic
def remove_member(*, user):
    user.delete()
    