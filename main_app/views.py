from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from .models import Profile, Post, Like
from .serializers import ProfileSerializer, PostSerializer, LikeSerializer
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


# copy and pasted the imports from cat collector :)

User = get_user_model()


class Home(APIView):
    def get(self, request):
        return Response({"message": "api"})


class ProfileIndex(APIView):
    def get(self, request):
        try:
            queryset = Profile.objects.all()
            serializer = ProfileSerializer(queryset, many=True)
            return Response(serializer.data)
        except Exception as err:
            return Response(
                {"error": str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def post(self, request):
        try:
            serializer = ProfileSerializer(data=request.data)
            if serializer.is_valid():
                print(request.user)
                serializer.save(user=request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as err:
            return Response(
                {"error": str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ProfileDetail(APIView):
    def get(self, request, user_id):
        try:
            profile = get_object_or_404(Profile, user__id=user_id)
            serializer = ProfileSerializer(profile)
            return Response(serializer.data)
        except Exception as err:
            return Response(
                {"error": str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def patch(self, request, user_id):
        try:
            profile = get_object_or_404(Profile, user__id=user_id)
            serializer = ProfileSerializer(profile, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                print(serializer.data)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as err:
            return Response(
                {"error": str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def delete(self, request, user_id):
        try:
            profile = get_object_or_404(Profile, user__id=user_id)
            if request.user != profile.user:
                return Response(
                    {"error": "you only can delete your account."},
                    status=status.HTTP_401_UNAUTHORIZED,
                )
            profile.user.delete()
            return Response(
                {"detail": "User and Profile has been deleted successfully"},
                status=status.HTTP_202_ACCEPTED,
            )
        except Exception as err:
            return Response(
                {"error": str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class PostIndex(APIView):
    def get(self, request):
        try:
            queryset = Post.objects.all()
            serializer = PostSerializer(queryset, many=True)
            return Response(serializer.data)
        except Exception as err:
            return Response(
                {"error": str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def post(self, request):
        try:
            serializer = PostSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(user=request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as err:
            return Response(
                {"error": str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class PostDetail(APIView):
    def get(self, request, post_id):
        try:
            post = get_object_or_404(Post, id=post_id)
            serializer = PostSerializer(post)
            return Response(serializer.data)
        except Exception as err:
            return Response(
                {"error": str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def patch(self, request, post_id):
        try:
            post = get_object_or_404(Post, id=post_id)
            if request.user != post.user:
                return Response(
                    {"error": "you only can only edit your own posts."},
                    status=status.HTTP_401_UNAUTHORIZED,
                )
            serializer = PostSerializer(post, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as err:
            return Response(
                {"error": str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def delete(self, request, post_id):
        try:
            post = get_object_or_404(Post, id=post_id)
            if request.user != post.user:
                return Response(
                    {"error": "you only can delete your own posts."},
                    status=status.HTTP_401_UNAUTHORIZED,
                )
            post.delete()
            return Response(
                {"detail": "Post has ben deleted seccessfully."},
                status=status.HTTP_202_ACCEPTED,
            )
        except Exception as err:
            return Response(
                {"error": str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# https://stackoverflow.com/questions/55434253/how-to-create-a-like-functionality-in-django-for-a-blog
class LikePost(APIView):
    def post(self, request, post_id):
        try:
            post = get_object_or_404(Post, id=post_id)
            like, created = Like.objects.get_or_create(user=request.user, post=post)
            if not created:
                return Response(
                    {"detail": "You allready liked this post."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            serializer = LikeSerializer(like)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as err:
            return Response(
                {"error": str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def delete(self, request, post_id):
        try:
            post = get_object_or_404(Post, id=post_id)
            like = Like.objects.filter(user=request.user, post=post).get()
            if not like:
                return Response(
                    {"detail": "You have not liked this post."},
                    status=status.HTTP_404_NOT_FOUND,
                )
            like.delete()
            return Response(
                {"detail": "Like removed."}, status=status.HTTP_202_ACCEPTED
            )
        except Exception as err:
            return Response(
                {"error": str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class LikeIndex(APIView):
    def get(self, request, post_id):
        try:
            post = get_object_or_404(Post, id=post_id)
            # related_name="likes"
            likes = post.likes.all()
            serializer = LikeSerializer(likes, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as err:
            return Response(
                {"error": str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class SignupUserView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        email = request.data.get("email")
        password = request.data.get("password")
        if not username or not password or not email:
            return Response(
                {"error": "Plesase provide a username, password, and email."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if User.objects.filter(username=username).exists():
            return Response(
                {"error": "this user already exists."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        user = User.objects.create_user(
            username=username, email=email, password=password
        )

        return Response(
            {"id": user.id, "username": user.username, "email": user.email},
            status=status.HTTP_201_CREATED,
        )
