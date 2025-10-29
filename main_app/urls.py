from django.urls import path
from .views import (
    Home,
    LikeIndex,
    LikePost,
    PostDetail,
    PostIndex,
    ProfileDetail,
    ProfileIndex,
    SignupUserView,
)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path("", Home.as_view(), name="home"),
    path("profile/<int:user_id>/", ProfileDetail.as_view(), name="profile_detail"),
    path("profiles/", ProfileIndex.as_view(), name="profile_index"),
    path("posts/", PostIndex.as_view(), name="posts"),
    path("posts/<int:post_id>", PostDetail.as_view(), name="posts"),
    path("posts/<int:post_id>/like/", LikePost.as_view(), name="like"),
    path("posts/<int:post_id>/likes/", LikeIndex.as_view(), name="likes"),
    path("login/", TokenObtainPairView.as_view(), name="login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("signup/", SignupUserView.as_view(), name="signup"),
]
