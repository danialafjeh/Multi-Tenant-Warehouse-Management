from django.contrib.auth.models import User
from django.db import transaction
from accounts.models import UserSnapshot
from .models import Membership
from organizations.models import Organization, Membership
from products.models import Category, UnitOfMeasure, Product
from stock.models import Inventory, StockMovement
from warehouses.models import Warehouse


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



@transaction.atomic
def delete_organization(*, organization_id):
    organization = (
        Organization.objects
        .select_for_update()
        .get(pk=organization_id)
    )

    # Collect user IDs before deleting memberships.
    member_user_ids = list(
        Membership.objects
        .filter(organization=organization)
        .values_list("user_id", flat=True)
    )

    # Delete stock history first because it protects
    # the organization, products, warehouses and snapshots.
    StockMovement.objects.filter(
        organization=organization,
    ).delete()

    # Delete inventory records before their related products
    # and warehouses.
    Inventory.objects.filter(
        organization=organization,
    ).delete()

    # Products protect their categories and units of measure.
    Product.objects.filter(
        organization=organization,
    ).delete()

    # Warehouses can now be deleted.
    Warehouse.objects.filter(
        organization=organization,
    ).delete()

    # Delete organization-specific reference data.
    Category.objects.filter(
        organization=organization,
    ).delete()

    UnitOfMeasure.objects.filter(
        organization=organization,
    ).delete()

    # Remove organization memberships.
    Membership.objects.filter(
        organization=organization,
    ).delete()

    # Delete the accounts belonging to this organization.
    # UserSnapshot.user uses SET_NULL, so snapshots survive.
    User.objects.filter(
        pk__in=member_user_ids,
    ).delete()

    # Delete the organization only after its protected
    # dependencies have been removed.
    organization.delete()
