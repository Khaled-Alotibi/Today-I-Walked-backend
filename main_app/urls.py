from django.urls import path
from .views import Home, PostDetail, PostIndex, ProfileDetail, ProfileIndex

urlpatterns = [
    path("", Home.as_view(), name="home"),
    path("profile/<int:user_id>/", ProfileDetail.as_view(), name="profile_detail"),
    path("profiles/", ProfileIndex.as_view(), name="profile_index"),
    path("posts/", PostIndex.as_view(), name="posts"),
    path("posts/<int:post_id>", PostDetail.as_view(), name="posts"),
]
