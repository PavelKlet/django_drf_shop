from rest_framework import serializers
from django.contrib.auth.models import User

from .models import Avatar, Profile


class AvatarSerializer(serializers.ModelSerializer):

    """Сериализатор аватара профиля"""

    src = serializers.SerializerMethodField()

    class Meta:
        model = Avatar
        fields = ["src", "alt"]

    def get_src(self, obj):
        return obj.src.url


class ProfileSerializer(serializers.ModelSerializer):

    """Сериализатор профиля"""

    avatar = AvatarSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = [
            "fullName",
            "email",
            "phone",
            "avatar",
        ]

    def create(self, validated_data):
        avatar = Avatar.objects.create(alt="Аватар пользователя")
        return Profile.objects.create(
            avatar=avatar,
            user=self.context["user"],
            fullName=validated_data["fullName"],
        )


class UserSerializer(serializers.ModelSerializer):

    """Сериализатор пользователя"""

    password = serializers.CharField(write_only=True)
    name = serializers.CharField(source="first_name")

    class Meta:
        model = User
        fields = ["name", "username", "password"]

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
