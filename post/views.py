from django.db.models import Q
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from post.models import Post
from post.serializers import PostSerializer
from user.models import UserFollowing


class PostViewSet(ModelViewSet):
    """Post CRUD endpoints"""
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    @action(
        methods=["POST"],
        detail=True,
        url_path="upload-image",
    )
    def upload_image(self, request, pk=None):
        """Endpoint for uploading image to specific movie"""
        play = self.get_object()
        serializer = self.get_serializer(play, data=request.data)

        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_queryset(self):
        following_queryset = UserFollowing.objects.filter(
            user_id=self.request.user
        )
        following_users_ids = [
            user.following_user_id.id for user in following_queryset
        ]
        queryset = (
            Post.objects.filter(
                Q(user_id__in=following_users_ids) | Q(user=self.request.user)
            )
            .prefetch_related("commentaries__user")
            .select_related("user")
        )
        hashtag = self.request.query_params.get("hashtag")

        if hashtag:
            queryset = queryset.filter(content__icontains=hashtag)

        return queryset

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return PostSerializer

        return super().get_serializer_class()

    def perform_create(
        self,
        serializer,
    ) -> None:
        serializer.save(user=self.request.user)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="hashtag",
                description="Filter by hashtag insensitive contains (ex. ?hashtag=post)",
                type=OpenApiTypes.STR,
            ),
        ]
    )
    def list(self, request, *args, **kwargs) -> Response:
        """List characters with filter by hashtag"""
        return super().list(request, *args, **kwargs)
