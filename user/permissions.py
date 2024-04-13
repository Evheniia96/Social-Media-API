from rest_framework.permissions import BasePermission, SAFE_METHODS
from user.models import UserFollowing


class IsOwnerFollowing(BasePermission):
    """Permissions for users owners"""

    def has_permission(self, request, view) -> bool:
        if (
            request.user.is_anonymous and request.method in SAFE_METHODS
        ) or request.user.is_authenticated:
            return True

    def has_object_permission(
        self, request, view, obj: UserFollowing
    ) -> bool:
        if request.method in SAFE_METHODS:
            return True

        return obj.user_id == request.user
