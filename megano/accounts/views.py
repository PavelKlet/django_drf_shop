import json

from rest_framework.views import APIView, Response, Request
from django.contrib.auth import authenticate, login, logout
from rest_framework import status
from rest_framework import permissions
from django.core.files.storage import default_storage
import PIL
from rest_framework.exceptions import ValidationError
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer

from .serializers import ProfileSerializer, UserSerializer
from .models import Profile, Avatar


class SignInAPIView(APIView):

    """Представление входа пользователя"""

    def post(self, request: Request) -> Response:
        user_data = json.loads(request.body)
        username = user_data.get("username")
        password = user_data.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SignUpAPIView(APIView):

    """Представление регистрации"""

    def post(self, request: Request) -> Response:
        data = json.loads(request.body)
        serializer = UserSerializer(data=data)
        if not serializer.is_valid():
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = serializer.save()
        profile_data = {
            "fullName": user.first_name,
        }
        profile_serializer = ProfileSerializer(
            context={"user": user}, data=profile_data
        )
        if not profile_serializer.is_valid():
            return Response(
                data=profile_serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )
        profile_serializer.save()
        user = authenticate(request, username=user.username, password=data["password"])
        if user:
            login(request, user)
            return Response(status=status.HTTP_201_CREATED)

        return Response(
            status=status.HTTP_500_INTERNAL_SERVER_ERROR, data="Ошибка при регистрации"
        )


@api_view(("POST",))
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def signout(request):
    """Представление выхода пользователя"""

    logout(request)
    return Response(status=status.HTTP_200_OK)


class ProfileAPIView(APIView):

    """Представление профиля пользователя"""

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request: Request) -> Response:
        profile = Profile.objects.get(user=request.user)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)

    def post(self, request: Request) -> Response:
        profile = Profile.objects.get(user=request.user)
        serializer = ProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AvatarUpdateAPIView(APIView):

    """Представление обновления аватара пользователя"""

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request: Request) -> Response:
        try:
            avatar = request.FILES["avatar"]
            PIL.Image.open(avatar)
            if avatar.size <= 2 * 1024 * 1024:
                profile = Profile.objects.get(user_id=request.user.pk)
                new_avatar = Avatar.objects.get(pk=profile.avatar_id)
                if new_avatar.src and (new_avatar.src != new_avatar.src.field.default):
                    old_avatar_path = new_avatar.src.path
                    if default_storage.exists(old_avatar_path):
                        default_storage.delete(old_avatar_path)
                new_avatar.src.save(avatar.name, avatar)
                return Response(status.HTTP_200_OK)
            raise ValidationError("Ошибка при сохранении изображения")
        except PIL.UnidentifiedImageError:
            return Response(
                {"error": "Ошибка при сохранении изображения"},
                status.HTTP_400_BAD_REQUEST,
            )


class UpdatePasswordAPIView(APIView):

    """Представление обновления пароля пользователя"""

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request: Request) -> Response:
        current_password = request.data.get("currentPassword")
        new_password = request.data.get("newPassword")
        if not request.user.check_password(current_password):
            return Response(
                {"error": "Ошибка при сохранении пароля"}, status.HTTP_400_BAD_REQUEST
            )
        request.user.set_password(new_password)
        request.user.save()
        return Response(status.HTTP_200_OK)
