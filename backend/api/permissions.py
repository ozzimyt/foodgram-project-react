from rest_framework.permissions import SAFE_METHODS, IsAuthenticatedOrReadOnly


class AuthorOrAdminOrReadOnly(IsAuthenticatedOrReadOnly):
    """Право доступа только для автора или администратора."""

    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS
            or request.user.is_authenticated
            and request.user == obj.author
        )
