import uuid
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)
from django.utils import timezone


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address")

        email = self.normalize_email(email)

        user = self.model(
            email=email,
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    email = models.EmailField(
        unique=True,
        db_index=True
    )

    # personalization
    preferred_name = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        help_text="Name used for personalization"
    )

    date_of_birth = models.DateField(
        blank=True,
        null=True,
        help_text="Date of birth"
    )

    # roles (future: therapist accounts)
    class Role(models.TextChoices):
        USER = "user", "User"
        THERAPIST = "therapist", "Therapist"
        ADMIN = "admin", "Admin"

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.USER
    )

    # verification
    is_email_verified = models.BooleanField(default=False)

    # onboarding
    is_onboarding_completed = models.BooleanField(
        default=False
    )

    # permissions
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # timestamps
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    last_active = models.DateTimeField(
        blank=True,
        null=True
    )

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return self.email