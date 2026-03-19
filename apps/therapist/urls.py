from django.urls import path
from .views import therapist_list

urlpatterns = [
    path("", therapist_list, name="therapist-list"),
]