from django.contrib.auth import get_user_model
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import generics, status, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import ValidationError
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.settings import api_settings

from user.models import UserFollowing
from user.permissions import IsOwnerFollowing
from user.serializers import UserSerializer, AuthTokenSerializer, FollowingSerializer


class UserPagination(PageNumberPagination):
    page_size = 2
    max_page_size = 100


class CreateUserView(generics.ListCreateAPIView):
    serializer_class = UserSerializer
    pagination_class = UserPagination

    def get_queryset(self):
        queryset = get_user_model().objects.prefetch_related(
            "following",
            "followers",
        )
        nickname = self.request.query_params.get("nickname")
        if nickname:
            queryset = queryset.filter(nickname__icontains=nickname)

        return queryset

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="nickname",
                type=OpenApiTypes.STR,
                description="Filtering by nickname (ex. ?nickname=monika)",
            ),
        ]
    )
    def get(self, request: Request, *args: tuple, **kwargs: dict) -> Response:
        return super().list(request, *args, **kwargs)


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


class UserFollowingViewSet(viewsets.ModelViewSet):
    """Following users"""

    serializer_class = FollowingSerializer
    queryset = UserFollowing.objects.prefetch_related("user_id", "following_user_id")
    permission_classes = (IsOwnerFollowing,)

    def create(
        self, request: Request, *args: tuple, **kwargs: dict
    ) -> ValidationError | Response:
        if self.request.user.email != request.data["user_id"]:
            raise ValidationError("You cannot sign other users!")

        return super().create(request, *args, **kwargs)
