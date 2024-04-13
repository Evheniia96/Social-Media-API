from django.contrib.auth import get_user_model
from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.settings import api_settings

from user.serializers import UserSerializer, AuthTokenSerializer


class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer


class LoginUserView(ObtainAuthToken):
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
    serializer_class = AuthTokenSerializer


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def logout(request):
    try:
        token = Token.objects.get(user=request.user)
        token.delete()
        return Response(
            {"message": "Successfully logged out"}, status=status.HTTP_200_OK
        )
    except Token.DoesNotExist:
        return Response({"error": "Token not found"}, status=status.HTTP_404_NOT_FOUND)


class ManageUserView(generics.RetrieveUpdateDestroyAPIView):
    """Update user witch already login"""

    serializer_class = UserSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user


class RetrieveUserView(generics.RetrieveAPIView):
    """Retrieve user witch already login"""

    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
