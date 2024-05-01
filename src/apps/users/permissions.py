from rest_framework.permissions import BasePermission


class IsAdminOrOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return bool(request.user.is_staff or request.user == obj.customer.user)
