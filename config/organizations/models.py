from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Organization(models.Model):
    name = models.CharField(
        max_length=150,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "Organization"
        verbose_name_plural = "Organizations"

    def __str__(self):
        return self.name



class Membership(models.Model):
    ROLE_CHOICES = [
        ("manager", "Manager"),
        ("staff", "Staff"),
        ("viewer", "Viewer"),
    ]
    
    organization = models.ForeignKey(
        Organization,
        on_delete=models.PROTECT,
        related_name="memberships",
    )
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="membership",
    )
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default="viewer",
    )
    is_active = models.BooleanField(
        default=True,
    )
    joined_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        ordering = ["joined_at"]
        verbose_name = "Membership"
        verbose_name_plural = "Memberships"

    def __str__(self):
        return f"{self.user.username} - {self.organization.name}"
    