from django.urls import path, include
from rest_framework import routers

from post.views import PostViewSet

router = routers.DefaultRouter()
router.register("posts", PostViewSet, basename="post")

urlpatterns = router.urls

app_name = "post"
