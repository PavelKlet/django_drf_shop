from django.urls import path

from .views import (
    SignInAPIView,
    SignUpAPIView,
    signout,
    ProfileAPIView,
    AvatarUpdateAPIView,
    UpdatePasswordAPIView,
)

appname = "accounts"

urlpatterns = [
    path("sign-in", SignInAPIView.as_view(), name="login"),
    path("sign-up", SignUpAPIView.as_view(), name="register"),
    path("sign-out", signout, name="logout"),
    path("profile", ProfileAPIView.as_view(), name="profile"),
    path("profile/avatar", AvatarUpdateAPIView.as_view(), name="update-avatar"),
    path("profile/password", UpdatePasswordAPIView.as_view(), name="update-password"),
]
