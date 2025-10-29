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


# copy and pasted the imports from cat collector :)
class Home(APIView):
    def get(self, request):
        return Response({"message": "api"})


class ProfileIndex(APIView):
    def get(self, request):
        queryset = Profile.objects.all()
        serializer = ProfileSerializer(queryset, many=True)
        return Response(serializer.data)

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
        profile = get_object_or_404(Profile, user__id=user_id)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)


class PostIndex(APIView):
    def get(self, request):
        queryset = Post.objects.all()
        serializer = PostSerializer(queryset, many=True)
        return Response(serializer.data)
