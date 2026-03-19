from django.contrib import admin
from django.utils.html import format_html
from .models import Therapist


@admin.register(Therapist)
class TherapistAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "image_preview",
        "name",
        "specialization",
        "is_verified",
    )

    list_filter = ("is_verified", "specialization")

    search_fields = ("name", "specialization", "location")

    ordering = ("-rating", "-created_at")

    fieldsets = (
        ("Basic Info", {
            "fields": ("name", "specialization", "bio")
        }),
        ("Details", {
            "fields": ("location", "availability", "rating")
        }),
        ("Status", {
            "fields": ("is_verified",)
        }),
        ("Media", {
            "fields": ("image",)
        }),
    )

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width:30px;height:30px;border-radius:5px;" />',
                obj.image.url
            )
        return "—"

    image_preview.short_description = "Image"