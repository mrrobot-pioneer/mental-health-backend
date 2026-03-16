from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import get_user_model

User = get_user_model()

class UpdateLastActiveMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        if request.user.is_authenticated:
            if not request.user.last_active or timezone.now() - request.user.last_active > timedelta(minutes=1):
                # update safely using queryset (avoids save errors)
                User.objects.filter(pk=request.user.pk).update(
                    last_active=timezone.now()
                )

        response = self.get_response(request)
        return response