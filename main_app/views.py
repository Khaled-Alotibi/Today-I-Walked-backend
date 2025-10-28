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
