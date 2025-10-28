from django.urls import path
from .views import Home, ProfileDetail, ProfileIndex

urlpatterns = [
    path("", Home.as_view(), name="home"),
    path("profile/<int:user_id>/", ProfileDetail.as_view(), name="profile_detail"),
    path("profiles/", ProfileIndex.as_view(), name="profile_index"),
]
