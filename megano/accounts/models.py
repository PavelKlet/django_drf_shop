from django.db import models
from django.contrib.auth.models import User


def path_avatar(instance: "Avatar", filename: str) -> str:
    """Функция генерации уникального пути к изображению"""

    return f"app_users/avatars/user_avatars/{instance.pk}/{filename}"


class Avatar(models.Model):

    """Модель для хранения аватара пользователя"""

    src = models.ImageField(
        upload_to=path_avatar,
        default="app_users/avatars/default.png",
        verbose_name="Ссылка",
    )
    alt = models.CharField(max_length=128, verbose_name="Описание")

    class Meta:
        verbose_name = "Аватар"
        verbose_name_plural = "Аватары"


class Profile(models.Model):

    """Модель профиля пользователя"""

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    fullName = models.CharField(max_length=128, verbose_name="Полное имя")
    phone = models.CharField(
        blank=True, null=True, unique=True, verbose_name="Номер телефона", max_length=12
    )
    email = models.EmailField(blank=True, null=True, max_length=100, unique=True)
    balance = models.DecimalField(
        decimal_places=2, max_digits=10, default=0, verbose_name="Баланс"
    )
    avatar = models.OneToOneField(
        Avatar,
        on_delete=models.CASCADE,
        related_name="profile",
        verbose_name="Аватар",
    )
