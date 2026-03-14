from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import RegisterSerializer, LoginSerializer


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
@permission_classes([IsAuthenticated])
def logout_user(request):

    try:
        refresh_token = request.data["refresh"]

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