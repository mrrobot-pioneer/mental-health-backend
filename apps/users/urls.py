from django.urls import path
from .views import register_user, submit_onboarding, login_user, logout_user, get_me
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path("register/", register_user, name="register"),
    path("onboarding/", submit_onboarding, name="onboarding"),
    path("login/", login_user, name="login"),
    path("refresh/", TokenRefreshView.as_view(), name="refresh"),
    path("logout/", logout_user, name="logout"),
    path("me/", get_me, name="me"),
]