import os
import uuid
from typing import Any, Optional

from django.contrib.auth import get_user_model
from django.contrib.auth.models import (
    AbstractUser,
    BaseUserManager,
)
from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext as _


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email: str, password: str, **extra_fields: Any):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(
        self,
        email: str,
        password: Optional[str] = None,
        **extra_fields: Any,
    ):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email: str, password: str, **extra_fields: Any):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


def user_image_file_path(instance, filename: str) -> str:
    _, extension = os.path.splitext(filename)
    filename = f"{slugify(instance.email)}-{uuid.uuid4()}{extension}"

    return os.path.join("uploads/posts/users/", filename)


class User(AbstractUser):
    username = None
    nickname = models.CharField(_("nickname"), max_length=15, unique=True)
    date_of_birth = models.DateField(_("date of birth"), null=True, blank=True)
    biography = models.CharField(_("short biography"), max_length=400, blank=True)
    email = models.EmailField(_("email address"), unique=True)
    profile_image = models.ImageField(blank=True, upload_to=user_image_file_path)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()


class UserFollowing(models.Model):
    user_id = models.ForeignKey(
        get_user_model(),
        related_name="following",
        on_delete=models.CASCADE,
    )
    following_user_id = models.ForeignKey(
        get_user_model(),
        related_name="followers",
        on_delete=models.CASCADE,
    )
    created = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user_id", "following_user_id"],
                name="unique_followers",
            )
        ]

        ordering = ["-created"]

    def __str__(self) -> str:
        return f"{self.user_id} follows {self.following_user_id}"
