from rest_framework import serializers
from .models import User
from django.contrib.auth import authenticate


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