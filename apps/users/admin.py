from django.contrib import admin
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "email",
        "preferred_name",
        "role",
        "is_email_verified",
        "created_at",
    )