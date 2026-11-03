from unittest.mock import patch
from django.contrib.auth.models import User
from django.db import IntegrityError, transaction
from django.test import TestCase
from django.urls import reverse
from accounts.models import UserSnapshot
from organizations.forms import AddMemberForm
from organizations.models import Organization, Membership
from organizations.services import (
    create_member,
    remove_member,
    delete_organization,
)
from products.models import (
    Category,
    UnitOfMeasure,
    Product,
    ProductSnapshot,
)
from stock.models import (
    Inventory,
    StockMovement,
)
from warehouses.models import Warehouse

# Create your tests here.

# ==========================================================
# Shared test data
# ==========================================================

class OrganizationTestDataMixin:

    def setUp(self):
        self.organization_a = Organization.objects.create(
            name="Organization A"
        )

        self.organization_b = Organization.objects.create(
            name="Organization B"
        )

        self.manager_a = User.objects.create_user(
            username="manager_a",
            password="TestPassword123!"
        )

        self.staff_a = User.objects.create_user(
            username="staff_a",
            password="TestPassword123!"
        )

        self.viewer_a = User.objects.create_user(
            username="viewer_a",
            password="TestPassword123!"
        )

        self.manager_b = User.objects.create_user(
            username="manager_b",
            password="TestPassword123!"
        )

        self.staff_b = User.objects.create_user(
            username="staff_b",
            password="TestPassword123!"
        )

        self.user_without_membership = User.objects.create_user(
            username="no_membership",
            password="TestPassword123!"
        )

        self.manager_a_membership = Membership.objects.create(
            organization=self.organization_a,
            user=self.manager_a,
            role="manager"
        )

        self.staff_a_membership = Membership.objects.create(
            organization=self.organization_a,
            user=self.staff_a,
            role="staff"
        )

        self.viewer_a_membership = Membership.objects.create(
            organization=self.organization_a,
            user=self.viewer_a,
            role="viewer"
        )

        self.manager_b_membership = Membership.objects.create(
            organization=self.organization_b,
            user=self.manager_b,
            role="manager"
        )

        self.staff_b_membership = Membership.objects.create(
            organization=self.organization_b,
            user=self.staff_b,
            role="staff"
        )

    def valid_member_data(self, **overrides):
        data = {
            "first_name": "New",
            "last_name": "Member",
            "username": "new_member",
            "email": "new_member@example.com",
            "role": "staff",
            "password1": "StrongPassword123!",
            "password2": "StrongPassword123!",
        }

        data.update(overrides)

        return data


# ==========================================================
# Organization model
# ==========================================================

class OrganizationModelTests(TestCase):

    def test_organization_can_be_created(self):
        organization = Organization.objects.create(
            name="Test Organization"
        )

        self.assertEqual(
            organization.name,
            "Test Organization"
        )

    def test_organization_string_representation(self):
        organization = Organization.objects.create(
            name="Test Organization"
        )

        self.assertEqual(
            str(organization),
            "Test Organization"
        )

    def test_organizations_are_ordered_by_name(self):
        Organization.objects.create(name="Zeta")
        Organization.objects.create(name="Alpha")

        organizations = list(
            Organization.objects.all()
        )

        self.assertEqual(
            organizations[0].name,
            "Alpha"
        )


# ==========================================================
# Membership model
# ==========================================================

class MembershipModelTests(
    OrganizationTestDataMixin,
    TestCase
):

    def test_membership_can_be_created(self):
        self.assertEqual(
            self.manager_a_membership.organization,
            self.organization_a
        )

    def test_membership_string_representation(self):
        self.assertEqual(
            str(self.manager_a_membership),
            "manager_a - Organization A"
        )

    def test_membership_role_choices_are_valid(self):
        valid_roles = {
            "manager",
            "staff",
            "viewer",
        }

        actual_roles = {
            role
            for role, label in Membership.ROLE_CHOICES
        }

        self.assertEqual(
            actual_roles,
            valid_roles
        )

    def test_user_can_have_only_one_membership(self):
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Membership.objects.create(
                    organization=self.organization_b,
                    user=self.manager_a,
                    role="staff"
                )

    def test_membership_default_role_is_viewer(self):
        user = User.objects.create_user(
            username="default_role_user",
            password="TestPassword123!"
        )

        membership = Membership.objects.create(
            organization=self.organization_a,
            user=user
        )

        self.assertEqual(
            membership.role,
            "viewer"
        )


# ==========================================================
# Members management page
# ==========================================================

class MembersManagementPageTests(
    OrganizationTestDataMixin,
    TestCase
):

    def test_manager_sees_only_members_of_own_organization(self):
        self.client.force_login(self.manager_a)

        response = self.client.get(
            reverse("members_management_page")
        )

        self.assertEqual(
            response.status_code,
            200
        )

        usernames = set(
            response.context["members"].values_list(
                "user__username",
                flat=True
            )
        )

        self.assertEqual(
            usernames,
            {
                "manager_a",
                "staff_a",
                "viewer_a",
            }
        )

        self.assertNotIn(
            "manager_b",
            usernames
        )

        self.assertNotIn(
            "staff_b",
            usernames
        )

    def test_staff_sees_only_members_of_own_organization(self):
        self.client.force_login(self.staff_a)

        response = self.client.get(
            reverse("members_management_page")
        )

        self.assertEqual(
            response.status_code,
            200
        )

        usernames = set(
            response.context["members"].values_list(
                "user__username",
                flat=True
            )
        )

        self.assertEqual(
            usernames,
            {
                "manager_a",
                "staff_a",
                "viewer_a",
            }
        )

        self.assertNotIn(
            "manager_b",
            usernames
        )

    def test_user_without_membership_is_redirected(self):
        self.client.force_login(
            self.user_without_membership
        )

        response = self.client.get(
            reverse("members_management_page")
        )

        self.assertEqual(
            response.status_code,
            302
        )

        self.assertRedirects(
            response,
            reverse("home_page"),
            fetch_redirect_response=False
        )

    def test_anonymous_user_is_redirected(self):
        response = self.client.get(
            reverse("members_management_page")
        )

        self.assertEqual(
            response.status_code,
            302
        )

        self.assertRedirects(
            response,
            reverse("home_page"),
            fetch_redirect_response=False
        )


# ==========================================================
# AddMemberForm
# ==========================================================

class AddMemberFormTests(TestCase):

    def valid_data(self, **overrides):
        data = {
            "first_name": "New",
            "last_name": "Member",
            "username": "new_member",
            "email": "new_member@example.com",
            "role": "staff",
            "password1": "StrongPassword123!",
            "password2": "StrongPassword123!",
        }

        data.update(overrides)

        return data

    def test_valid_form_is_accepted(self):
        form = AddMemberForm(
            data=self.valid_data()
        )

        self.assertTrue(
            form.is_valid(),
            form.errors
        )

    def test_password_mismatch_is_rejected(self):
        form = AddMemberForm(
            data=self.valid_data(
                password2="DifferentPassword123!"
            )
        )

        self.assertFalse(
            form.is_valid()
        )

        self.assertIn(
            "password2",
            form.errors
        )

    def test_invalid_email_is_rejected(self):
        form = AddMemberForm(
            data=self.valid_data(
                email="invalid-email"
            )
        )

        self.assertFalse(
            form.is_valid()
        )

        self.assertIn(
            "email",
            form.errors
        )

    def test_invalid_role_is_rejected(self):
        form = AddMemberForm(
            data=self.valid_data(
                role="manager"
            )
        )

        self.assertFalse(
            form.is_valid()
        )

        self.assertIn(
            "role",
            form.errors
        )

    def test_duplicate_username_is_rejected(self):
        User.objects.create_user(
            username="new_member",
            password="ExistingPassword123!"
        )

        form = AddMemberForm(
            data=self.valid_data()
        )

        self.assertFalse(
            form.is_valid()
        )

        self.assertIn(
            "username",
            form.errors
        )


# ==========================================================
# Add member view
# ==========================================================

class AddMemberViewTests(
    OrganizationTestDataMixin,
    TestCase
):

    def test_manager_can_add_member_to_own_organization(self):
        self.client.force_login(
            self.manager_a
        )

        response = self.client.post(
            reverse("add_member_system"),
            data=self.valid_member_data()
        )

        self.assertEqual(
            response.status_code,
            302
        )

        self.assertRedirects(
            response,
            reverse("members_management_page"),
            fetch_redirect_response=False
        )

        new_user = User.objects.get(
            username="new_member"
        )

        membership = Membership.objects.get(
            user=new_user
        )

        self.assertEqual(
            membership.organization,
            self.organization_a
        )

        self.assertEqual(
            membership.role,
            "staff"
        )

        self.assertTrue(
            new_user.check_password(
                "StrongPassword123!"
            )
        )

        self.assertTrue(
            UserSnapshot.objects.filter(
                user=new_user
            ).exists()
        )

    def test_manager_can_add_viewer(self):
        self.client.force_login(
            self.manager_a
        )

        response = self.client.post(
            reverse("add_member_system"),
            data=self.valid_member_data(
                username="new_viewer",
                email="new_viewer@example.com",
                role="viewer"
            )
        )

        self.assertEqual(
            response.status_code,
            302
        )

        membership = Membership.objects.get(
            user__username="new_viewer"
        )

        self.assertEqual(
            membership.organization,
            self.organization_a
        )

        self.assertEqual(
            membership.role,
            "viewer"
        )

    def test_staff_cannot_add_member(self):
        self.client.force_login(
            self.staff_a
        )

        response = self.client.post(
            reverse("add_member_system"),
            data=self.valid_member_data()
        )

        self.assertEqual(
            response.status_code,
            302
        )

        self.assertFalse(
            User.objects.filter(
                username="new_member"
            ).exists()
        )

    def test_viewer_cannot_add_member(self):
        self.client.force_login(
            self.viewer_a
        )

        response = self.client.post(
            reverse("add_member_system"),
            data=self.valid_member_data()
        )

        self.assertEqual(
            response.status_code,
            302
        )

        self.assertFalse(
            User.objects.filter(
                username="new_member"
            ).exists()
        )

    def test_user_without_membership_cannot_add_member(self):
        self.client.force_login(
            self.user_without_membership
        )

        response = self.client.post(
            reverse("add_member_system"),
            data=self.valid_member_data()
        )

        self.assertEqual(
            response.status_code,
            302
        )

        self.assertFalse(
            User.objects.filter(
                username="new_member"
            ).exists()
        )

    def test_anonymous_user_cannot_add_member(self):
        response = self.client.post(
            reverse("add_member_system"),
            data=self.valid_member_data()
        )

        self.assertEqual(
            response.status_code,
            302
        )

        self.assertFalse(
            User.objects.filter(
                username="new_member"
            ).exists()
        )

    def test_invalid_form_does_not_create_user(self):
        self.client.force_login(
            self.manager_a
        )

        response = self.client.post(
            reverse("add_member_system"),
            data=self.valid_member_data(
                password2="DifferentPassword123!"
            )
        )

        self.assertEqual(
            response.status_code,
            302
        )

        self.assertFalse(
            User.objects.filter(
                username="new_member"
            ).exists()
        )

        self.assertFalse(
            Membership.objects.filter(
                user__username="new_member"
            ).exists()
        )

    def test_get_request_does_not_create_member(self):
        self.client.force_login(
            self.manager_a
        )

        response = self.client.get(
            reverse("add_member_system")
        )

        self.assertEqual(
            response.status_code,
            302
        )

        self.assertFalse(
            User.objects.filter(
                username="new_member"
            ).exists()
        )


# ==========================================================
# Remove member view
# ==========================================================

class RemoveMemberViewTests(
    OrganizationTestDataMixin,
    TestCase
):

    def test_manager_can_remove_member_from_own_organization(self):
        self.client.force_login(
            self.manager_a
        )

        response = self.client.post(
            reverse(
                "remove_member_system",
                kwargs={
                    "user_id": self.staff_a.id
                }
            )
        )

        self.assertEqual(
            response.status_code,
            302
        )

        self.assertFalse(
            User.objects.filter(
                username="staff_a"
            ).exists()
        )

        self.assertFalse(
            Membership.objects.filter(
                user=self.staff_a
            ).exists()
        )

    def test_manager_cannot_remove_member_from_another_organization(self):
        self.client.force_login(
            self.manager_a
        )

        response = self.client.post(
            reverse(
                "remove_member_system",
                kwargs={
                    "user_id": self.staff_b.id
                }
            )
        )

        self.assertEqual(
            response.status_code,
            404
        )

        self.assertTrue(
            Membership.objects.filter(
                user=self.staff_b,
                organization=self.organization_b
            ).exists()
        )

        self.assertTrue(
            User.objects.filter(
                username="staff_b"
            ).exists()
        )

    def test_staff_cannot_remove_member(self):
        self.client.force_login(
            self.staff_a
        )

        response = self.client.post(
            reverse(
                "remove_member_system",
                kwargs={
                    "user_id": self.viewer_a.id
                }
            )
        )

        self.assertEqual(
            response.status_code,
            302
        )

        self.assertTrue(
            Membership.objects.filter(
                user=self.viewer_a
            ).exists()
        )

    def test_viewer_cannot_remove_member(self):
        self.client.force_login(
            self.viewer_a
        )

        response = self.client.post(
            reverse(
                "remove_member_system",
                kwargs={
                    "user_id": self.staff_a.id
                }
            )
        )

        self.assertEqual(
            response.status_code,
            302
        )

        self.assertTrue(
            Membership.objects.filter(
                user=self.staff_a
            ).exists()
        )

    def test_manager_cannot_remove_themselves(self):
        self.client.force_login(
            self.manager_a
        )

        response = self.client.post(
            reverse(
                "remove_member_system",
                kwargs={
                    "user_id": self.manager_a.id
                }
            )
        )

        self.assertEqual(
            response.status_code,
            302
        )

        self.assertTrue(
            Membership.objects.filter(
                user=self.manager_a
            ).exists()
        )

    def test_anonymous_user_cannot_remove_member(self):
        response = self.client.post(
            reverse(
                "remove_member_system",
                kwargs={
                    "user_id": self.staff_a.id
                }
            )
        )

        self.assertEqual(
            response.status_code,
            302
        )

        self.assertTrue(
            Membership.objects.filter(
                user=self.staff_a
            ).exists()
        )

    def test_user_without_membership_cannot_remove_member(self):
        self.client.force_login(
            self.user_without_membership
        )

        response = self.client.post(
            reverse(
                "remove_member_system",
                kwargs={
                    "user_id": self.staff_a.id
                }
            )
        )

        self.assertEqual(
            response.status_code,
            404
        )

        self.assertTrue(
            Membership.objects.filter(
                user=self.staff_a
            ).exists()
        )

    def test_get_request_does_not_remove_member(self):
        self.client.force_login(
            self.manager_a
        )

        response = self.client.get(
            reverse(
                "remove_member_system",
                kwargs={
                    "user_id": self.staff_a.id
                }
            )
        )

        self.assertEqual(
            response.status_code,
            302
        )

        self.assertTrue(
            Membership.objects.filter(
                user=self.staff_a
            ).exists()
        )


# ==========================================================
# Delete organization view
# ==========================================================

class DeleteOrganizationViewTests(
    OrganizationTestDataMixin,
    TestCase
):

    @patch("organizations.views.delete_organization")
    def test_manager_can_delete_organization(
        self,
        mocked_delete_organization
    ):
        self.client.force_login(
            self.manager_a
        )

        response = self.client.post(
            reverse("delete_organization_system")
        )

        self.assertEqual(
            response.status_code,
            302
        )

        self.assertRedirects(
            response,
            reverse("home_page"),
            fetch_redirect_response=False
        )

        mocked_delete_organization.assert_called_once_with(
            organization_id=self.organization_a.id
        )

    @patch("organizations.views.delete_organization")
    def test_staff_cannot_delete_organization(
        self,
        mocked_delete_organization
    ):
        self.client.force_login(
            self.staff_a
        )

        response = self.client.post(
            reverse("delete_organization_system")
        )

        self.assertEqual(
            response.status_code,
            302
        )

        mocked_delete_organization.assert_not_called()

    @patch("organizations.views.delete_organization")
    def test_viewer_cannot_delete_organization(
        self,
        mocked_delete_organization
    ):
        self.client.force_login(
            self.viewer_a
        )

        response = self.client.post(
            reverse("delete_organization_system")
        )

        self.assertEqual(
            response.status_code,
            302
        )

        mocked_delete_organization.assert_not_called()

    @patch("organizations.views.delete_organization")
    def test_anonymous_user_cannot_delete_organization(
        self,
        mocked_delete_organization
    ):
        response = self.client.post(
            reverse("delete_organization_system")
        )

        self.assertEqual(
            response.status_code,
            302
        )

        mocked_delete_organization.assert_not_called()

    @patch("organizations.views.delete_organization")
    def test_get_request_cannot_delete_organization(
        self,
        mocked_delete_organization
    ):
        self.client.force_login(
            self.manager_a
        )

        response = self.client.get(
            reverse("delete_organization_system")
        )

        self.assertEqual(
            response.status_code,
            302
        )

        mocked_delete_organization.assert_not_called()

    def test_manager_can_access_delete_organization_page(self):
        self.client.force_login(
            self.manager_a
        )

        response = self.client.get(
            reverse("delete_organization_page")
        )

        self.assertEqual(
            response.status_code,
            200
        )

    def test_staff_cannot_access_delete_organization_page(self):
        self.client.force_login(
            self.staff_a
        )

        response = self.client.get(
            reverse("delete_organization_page")
        )

        self.assertEqual(
            response.status_code,
            302
        )

    def test_viewer_cannot_access_delete_organization_page(self):
        self.client.force_login(
            self.viewer_a
        )

        response = self.client.get(
            reverse("delete_organization_page")
        )

        self.assertEqual(
            response.status_code,
            302
        )

    def test_user_without_membership_cannot_access_delete_page(self):
        self.client.force_login(
            self.user_without_membership
        )

        response = self.client.get(
            reverse("delete_organization_page")
        )

        self.assertEqual(
            response.status_code,
            404
        )


# ==========================================================
# Organization services
# ==========================================================

class OrganizationServicesTests(
    OrganizationTestDataMixin,
    TestCase
):

    def test_create_member_creates_user_membership_and_snapshot(self):
        membership = create_member(
            first_name="Service",
            last_name="Member",
            username="service_member",
            email="service_member@example.com",
            password="StrongPassword123!",
            role="staff",
            organization=self.organization_a
        )

        self.assertEqual(
            membership.organization,
            self.organization_a
        )

        self.assertEqual(
            membership.role,
            "staff"
        )

        self.assertEqual(
            membership.user.username,
            "service_member"
        )

        self.assertTrue(
            membership.user.check_password(
                "StrongPassword123!"
            )
        )

        snapshot = UserSnapshot.objects.get(
            user=membership.user
        )

        self.assertEqual(
            snapshot.username,
            "service_member"
        )

        self.assertEqual(
            snapshot.first_name,
            "Service"
        )

        self.assertEqual(
            snapshot.last_name,
            "Member"
        )

    def test_remove_member_deletes_user_and_membership(self):
        user_id = self.staff_a.id

        snapshot = UserSnapshot.objects.create(
            user=self.staff_a,
            username=self.staff_a.username,
            first_name=self.staff_a.first_name,
            last_name=self.staff_a.last_name,
            email=self.staff_a.email,
        )

        remove_member(
            user=self.staff_a
        )

        self.assertFalse(
            User.objects.filter(
                id=user_id
            ).exists()
        )

        self.assertFalse(
            Membership.objects.filter(
                user_id=user_id
            ).exists()
        )

        # UserSnapshot survives because user uses SET_NULL.
        snapshot.refresh_from_db()

        self.assertTrue(
            UserSnapshot.objects.filter(
                pk=snapshot.pk
            ).exists()
        )

        self.assertIsNone(snapshot.user_id)


# ==========================================================
# Delete organization service
# ==========================================================

class DeleteOrganizationServiceTests(OrganizationTestDataMixin, TestCase):

    def test_delete_organization_removes_organization(self):
        organization_id = self.organization_a.id

        delete_organization(
            organization_id=organization_id
        )

        self.assertFalse(
            Organization.objects.filter(
                id=organization_id
            ).exists()
        )

    def test_delete_organization_does_not_delete_other_organization(self):
        delete_organization(
            organization_id=self.organization_a.id
        )

        self.assertTrue(
            Organization.objects.filter(
                id=self.organization_b.id
            ).exists()
        )

    def test_delete_organization_removes_memberships(self):
        organization_id = self.organization_a.id

        delete_organization(
            organization_id=organization_id
        )

        self.assertFalse(
            Membership.objects.filter(
                organization_id=organization_id
            ).exists()
        )

    def test_delete_organization_removes_users(self):
        user_ids = list(
            Membership.objects.filter(
                organization=self.organization_a
            ).values_list(
                "user_id",
                flat=True
            )
        )

        delete_organization(
            organization_id=self.organization_a.id
        )

        self.assertFalse(
            User.objects.filter(
                id__in=user_ids
            ).exists()
        )

    def test_delete_organization_preserves_user_snapshots(self):
        snapshots = list(
            UserSnapshot.objects.filter(
                user__membership__organization=self.organization_a
            )
        )

        delete_organization(
            organization_id=self.organization_a.id
        )

        for snapshot in snapshots:
            self.assertTrue(
                UserSnapshot.objects.filter(
                    id=snapshot.id
                ).exists()
            )

            self.assertIsNone(
                UserSnapshot.objects.get(
                    id=snapshot.id
                ).user
            )


# ==========================================================
# Complete organization deletion integration tests
# ==========================================================

class CompleteDeleteOrganizationServiceTests(OrganizationTestDataMixin, TestCase):

    def setUp(self):
        super().setUp()

        # --------------------------------------------------
        # Organization A reference data
        # --------------------------------------------------

        self.category_a = Category.objects.create(
            organization=self.organization_a,
            name="Electronics",
            description="Electronic products"
        )

        self.unit_a = UnitOfMeasure.objects.create(
            organization=self.organization_a,
            name="Piece",
            abbreviation="pcs"
        )

        self.warehouse_a = Warehouse.objects.create(
            organization=self.organization_a,
            name="Main Warehouse",
            code="WH-A"
        )

        self.product_a = Product.objects.create(
            organization=self.organization_a,
            category=self.category_a,
            unit=self.unit_a,
            name="Laptop",
            sku="LAPTOP-A",
            reorder_level="5.0",
            description="Test product"
        )

        self.inventory_a = Inventory.objects.create(
            organization=self.organization_a,
            warehouse=self.warehouse_a,
            product=self.product_a,
            quantity="20.0"
        )

        # --------------------------------------------------
        # Organization A snapshots
        # --------------------------------------------------

        self.product_snapshot_a = ProductSnapshot.objects.create(
            organization=self.organization_a,
            product=self.product_a,
            name=self.product_a.name,
            sku=self.product_a.sku,
            category_name=self.category_a.name,
            unit_name=self.unit_a.name,
            unit_abbreviation=self.unit_a.abbreviation,
            reorder_level=self.product_a.reorder_level,
            description=self.product_a.description
        )

        self.manager_snapshot_a = UserSnapshot.objects.create(
            user=self.manager_a,
            username=self.manager_a.username,
            first_name=self.manager_a.first_name,
            last_name=self.manager_a.last_name,
            email=self.manager_a.email
        )

        self.staff_snapshot_a = UserSnapshot.objects.create(
            user=self.staff_a,
            username=self.staff_a.username,
            first_name=self.staff_a.first_name,
            last_name=self.staff_a.last_name,
            email=self.staff_a.email
        )

        # --------------------------------------------------
        # Organization A stock movement
        # --------------------------------------------------

        self.stock_movement_a = StockMovement.objects.create(
            organization=self.organization_a,
            product_snapshot=self.product_snapshot_a,
            movement_type="stock_in",
            warehouse=self.warehouse_a,
            quantity="20.0",
            notes="Initial stock",
            recorded_by=self.manager_a,
            recorded_by_snapshot=self.manager_snapshot_a
        )

        # --------------------------------------------------
        # Organization B data
        # These records must survive deletion of A.
        # --------------------------------------------------

        self.category_b = Category.objects.create(
            organization=self.organization_b,
            name="Furniture"
        )

        self.unit_b = UnitOfMeasure.objects.create(
            organization=self.organization_b,
            name="Box",
            abbreviation="box"
        )

        self.warehouse_b = Warehouse.objects.create(
            organization=self.organization_b,
            name="Second Warehouse",
            code="WH-B"
        )

        self.product_b = Product.objects.create(
            organization=self.organization_b,
            category=self.category_b,
            unit=self.unit_b,
            name="Chair",
            sku="CHAIR-B",
            reorder_level="2.0"
        )

        self.inventory_b = Inventory.objects.create(
            organization=self.organization_b,
            warehouse=self.warehouse_b,
            product=self.product_b,
            quantity="10.0"
        )

        self.product_snapshot_b = ProductSnapshot.objects.create(
            organization=self.organization_b,
            product=self.product_b,
            name=self.product_b.name,
            sku=self.product_b.sku,
            category_name=self.category_b.name,
            unit_name=self.unit_b.name,
            unit_abbreviation=self.unit_b.abbreviation,
            reorder_level=self.product_b.reorder_level
        )

        self.manager_snapshot_b = UserSnapshot.objects.create(
            user=self.manager_b,
            username=self.manager_b.username,
            first_name=self.manager_b.first_name,
            last_name=self.manager_b.last_name,
            email=self.manager_b.email
        )

        self.stock_movement_b = StockMovement.objects.create(
            organization=self.organization_b,
            product_snapshot=self.product_snapshot_b,
            movement_type="stock_in",
            warehouse=self.warehouse_b,
            quantity="10.0",
            notes="Organization B stock",
            recorded_by=self.manager_b,
            recorded_by_snapshot=self.manager_snapshot_b
        )

    def test_delete_organization_removes_all_dependent_data(self):
        organization_id = self.organization_a.id

        delete_organization(
            organization_id=organization_id
        )

        self.assertFalse(
            Organization.objects.filter(
                id=organization_id
            ).exists()
        )

        self.assertFalse(
            Membership.objects.filter(
                organization_id=organization_id
            ).exists()
        )

        self.assertFalse(
            Category.objects.filter(
                organization_id=organization_id
            ).exists()
        )

        self.assertFalse(
            UnitOfMeasure.objects.filter(
                organization_id=organization_id
            ).exists()
        )

        self.assertFalse(
            Warehouse.objects.filter(
                organization_id=organization_id
            ).exists()
        )

        self.assertFalse(
            Product.objects.filter(
                organization_id=organization_id
            ).exists()
        )

        self.assertFalse(
            ProductSnapshot.objects.filter(
                organization_id=organization_id
            ).exists()
        )

        self.assertFalse(
            Inventory.objects.filter(
                organization_id=organization_id
            ).exists()
        )

        self.assertFalse(
            StockMovement.objects.filter(
                organization_id=organization_id
            ).exists()
        )

    def test_delete_organization_preserves_other_organization_data(self):
        delete_organization(
            organization_id=self.organization_a.id
        )

        self.assertTrue(
            Organization.objects.filter(
                id=self.organization_b.id
            ).exists()
        )

        self.assertTrue(
            Membership.objects.filter(
                organization=self.organization_b
            ).exists()
        )

        self.assertTrue(
            Category.objects.filter(
                organization=self.organization_b
            ).exists()
        )

        self.assertTrue(
            UnitOfMeasure.objects.filter(
                organization=self.organization_b
            ).exists()
        )

        self.assertTrue(
            Warehouse.objects.filter(
                organization=self.organization_b
            ).exists()
        )

        self.assertTrue(
            Product.objects.filter(
                organization=self.organization_b
            ).exists()
        )

        self.assertTrue(
            ProductSnapshot.objects.filter(
                organization=self.organization_b
            ).exists()
        )

        self.assertTrue(
            Inventory.objects.filter(
                organization=self.organization_b
            ).exists()
        )

        self.assertTrue(
            StockMovement.objects.filter(
                organization=self.organization_b
            ).exists()
        )

    def test_delete_organization_preserves_user_snapshots(self):
        manager_snapshot_id = self.manager_snapshot_a.id
        staff_snapshot_id = self.staff_snapshot_a.id

        delete_organization(
            organization_id=self.organization_a.id
        )

        manager_snapshot = UserSnapshot.objects.get(
            id=manager_snapshot_id
        )

        staff_snapshot = UserSnapshot.objects.get(
            id=staff_snapshot_id
        )

        self.assertIsNone(
            manager_snapshot.user
        )

        self.assertIsNone(
            staff_snapshot.user
        )

        self.assertEqual(
            manager_snapshot.username,
            "manager_a"
        )

        self.assertEqual(
            staff_snapshot.username,
            "staff_a"
        )

    def test_delete_organization_removes_organization_users(self):
        organization_user_ids = list(
            Membership.objects.filter(
                organization=self.organization_a
            ).values_list(
                "user_id",
                flat=True
            )
        )

        delete_organization(
            organization_id=self.organization_a.id
        )

        self.assertFalse(
            User.objects.filter(
                id__in=organization_user_ids
            ).exists()
        )

        self.assertTrue(
            User.objects.filter(
                id=self.manager_b.id
            ).exists()
        )

        self.assertTrue(
            User.objects.filter(
                id=self.staff_b.id
            ).exists()
        )

class DeleteOrganizationMissingRecordTests(TestCase):

    def test_deleting_nonexistent_organization_raises_error(self):
        with self.assertRaises(
            Organization.DoesNotExist
        ):
            delete_organization(
                organization_id=999999
            )
