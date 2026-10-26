from django.contrib.auth.models import User
from django.db import transaction
from organizations.models import Membership, Organization
from .models import UserSnapshot



@transaction.atomic
def register_user(*, first_name, last_name, username, email, password, organization_name):
    user = User.objects.create_user(
        username=username,
        first_name=first_name,
        last_name=last_name,
        email=email,
        password=password,
    )

    UserSnapshot.objects.create(
        user=user,
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
    )

    organization = Organization.objects.create(
        name=organization_name,
    )

    Membership.objects.create(
        organization=organization,
        user=user,
        role="manager",
        is_active=True,
    )

    return user