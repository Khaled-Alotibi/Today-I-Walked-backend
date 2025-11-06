from typing import Required
from rest_framework import serializers
from django.db.models import Sum
from .models import Profile, Post, Like


class ProfileSerializer(serializers.ModelSerializer):
    # https://stackoverflow.com/questions/58891872/how-to-get-a-username-to-show-on-serializer-django-rest-framework
    username = serializers.CharField(source="user.username", read_only=True)
    user_id = serializers.IntegerField(source="user.id", read_only=True)
    total_steps = serializers.SerializerMethodField()
    profile_pic = serializers.ImageField(required=False)

    class Meta:
        model = Profile
        fields = ["id", "user_id", "username", "bio", "profile_pic", "total_steps"]

    def get_total_steps(self, obj):
        return obj.user.posts.aggregate(total=Sum("steps"))["total"] or 0

    def get_profile_pic(self, obj):
        if obj.profile_pic:
            return obj.profile_pic.url
        return "/media/profile_pic/default-profile_pic.png"


class PostSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="author.username", read_only=True)
    user_id = serializers.IntegerField(source="author.id", read_only=True)
    likes_count = serializers.SerializerMethodField()
    liked_by = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            "id",
            "username",
            "image",
            "caption",
            "steps",
            "created_at",
            "likes_count",
            "liked_by",
            "user_id",
        ]

    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_liked_by(self, obj):
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            return obj.likes.filter(user=request.user).exists()
        return False


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = "__all__"
