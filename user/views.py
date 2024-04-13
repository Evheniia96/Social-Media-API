from django.contrib.auth import get_user_model
from django.shortcuts import render
from rest_framework import generics

from user.serializers import UserSerializer


class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer


class ManageUserView(generics.RetrieveUpdateDestroyAPIView):
    """Update user witch already login"""

    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class RetrieveUserView(generics.RetrieveAPIView):
    """Retrieve user witch already login"""

    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
