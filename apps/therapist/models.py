import uuid
from django.db import models


class Therapist(models.Model):
    id = models.UUIDField(
        primary_key=True, 
        default=uuid.uuid4, 
        editable=False
    )
    
    name = models.CharField(max_length=255)
    specialization = models.CharField(max_length=255)
    location = models.CharField(max_length=255, blank=True)
    bio = models.TextField(blank=True)
    image = models.ImageField(upload_to="therapists/")

    rating = models.FloatField(default=0)

    availability = models.CharField(max_length=255, blank=True)

    is_verified = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name