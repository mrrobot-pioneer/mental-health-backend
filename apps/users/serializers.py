from rest_framework import serializers
from .models import User
from django.contrib.auth import authenticate
from datetime import date


class RegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            "email",
            "password",
        ]

    def create(self, validated_data):
        password = validated_data.pop("password")

        user = User(**validated_data)
        user.set_password(password)
        user.save()

        return user


class OnboardingSerializer(serializers.Serializer):
    preferred_name = serializers.CharField(max_length=50)
    date_of_birth = serializers.DateField()

    def validate_preferred_name(self, value):
        value = value.strip()

        if not value:
            raise serializers.ValidationError("Preferred name cannot be empty.")

        if len(value) < 2:
            raise serializers.ValidationError(
                "Preferred name must be at least 2 characters."
            )

        if len(value) > 50:
            raise serializers.ValidationError(
                "Preferred name cannot exceed 50 characters."
            )

        return value

    def validate_date_of_birth(self, value):
        today = date.today()

        # Prevent future dates
        if value > today:
            raise serializers.ValidationError("Date of birth cannot be in the future.")

        # Age calculation
        age = today.year - value.year - (
            (today.month, today.day) < (value.month, value.day)
        )

        if age < 18:
            raise serializers.ValidationError("You must be at least 18 years old.")

        # sanity check for extremely old ages
        if age > 120:
            raise serializers.ValidationError("Invalid date of birth.")

        return value


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")

        user = authenticate(username=email, password=password)

        if not user:
            raise serializers.ValidationError("Invalid email or password")

        if not user.is_active:
            raise serializers.ValidationError("This account is disabled")

        data["user"] = user
        return data