from typing_extensions import ReadOnly
from rest_framework import serializers
from .models import Profile, Post, Like


class ProfileSerializer(serializers.ModelSerializer):
    # https://stackoverflow.com/questions/58891872/how-to-get-a-username-to-show-on-serializer-django-rest-framework
    username = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = Profile
        fields = "__all__"


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = "__all__"


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = "__all__"
