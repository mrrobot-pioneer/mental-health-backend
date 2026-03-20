from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import RegisterSerializer, OnboardingSerializer, LoginSerializer


@api_view(["POST"])
@permission_classes([AllowAny])
def register_user(request):

    serializer = RegisterSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    user = serializer.save()

    # create tokens immediately
    refresh = RefreshToken.for_user(user)

    return Response(
        {
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "user": {
                "id": str(user.id),
                "email": user.email,
                "preferred_name": user.preferred_name,
                "role": user.role,
                "is_onboarding_completed": user.is_onboarding_completed,
            },
        },
        status=status.HTTP_201_CREATED,
    )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def submit_onboarding(request):

    user = request.user

    if user.is_onboarding_completed:
        return Response(
            {"error": "Onboarding already completed"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    serializer = OnboardingSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    user.preferred_name = serializer.validated_data["preferred_name"]
    user.date_of_birth = serializer.validated_data["date_of_birth"]
    user.is_onboarding_completed = True
    user.save(update_fields=[
        "preferred_name",
        "date_of_birth",
        "is_onboarding_completed",
    ])

    return Response(
        {
            "id": str(user.id),
            "preferred_name": user.preferred_name,
            "is_onboarding_completed": user.is_onboarding_completed,
        },
        status=status.HTTP_200_OK,
    )


@api_view(["POST"])
@permission_classes([AllowAny])
def login_user(request):

    serializer = LoginSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    user = serializer.validated_data["user"]

    refresh = RefreshToken.for_user(user)

    return Response(
        {
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "user": {
                "id": str(user.id),
                "email": user.email,
                "preferred_name": user.preferred_name,
                "role": user.role,
                "is_onboarding_completed": user.is_onboarding_completed,
            },
        },
        status=status.HTTP_200_OK,
    )


@api_view(["POST"])
def logout_user(request):

    refresh_token = request.data.get("refresh")

    if not refresh_token:
        return Response(
            {"error": "Refresh token required"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        token = RefreshToken(refresh_token)
        token.blacklist()

        return Response(
            {"message": "Logout successful"},
            status=status.HTTP_205_RESET_CONTENT,
        )

    except Exception:
        return Response(
            {"error": "Invalid token"},
            status=status.HTTP_400_BAD_REQUEST,
        )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_me(request):

    user = request.user

    return Response(
        {
            "id": str(user.id),
            "email": user.email,
            "preferred_name": user.preferred_name,
            "role": user.role,
            "is_onboarding_completed": user.is_onboarding_completed,
        },
        status=status.HTTP_200_OK,
    )


@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
def update_me(request):
    user = request.user

    preferred_name = request.data.get("preferred_name")
    email = request.data.get("email")

    if preferred_name is not None:
        user.preferred_name = preferred_name

    if email is not None:
        user.email = email

    user.save()

    return Response(
        {
            "id": str(user.id),
            "email": user.email,
            "preferred_name": user.preferred_name,
            "role": user.role,
            "is_onboarding_completed": user.is_onboarding_completed,
        },
        status=status.HTTP_200_OK,
    )