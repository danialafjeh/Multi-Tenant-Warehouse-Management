from django.db import models
import uuid
from django.contrib.auth.models import User

# Create your models here.

class UserSnapshot(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    user = models.OneToOneField(
        User,
        on_delete=models.SET_NULL,
        related_name="snapshot",
        null=True,
        blank=True,
    )
    username = models.CharField(
        max_length=150,
    )
    first_name = models.CharField(
        max_length=150,
        blank=True,
    )
    last_name = models.CharField(
        max_length=150,
        blank=True,
    )
    email = models.EmailField(
        blank=True,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "User Snapshot"
        verbose_name_plural = "User Snapshots"

    def __str__(self):
        full_name = f"{self.first_name} {self.last_name}".strip()

        if full_name:
            return f"{full_name} ({self.username})"

        return self.username
