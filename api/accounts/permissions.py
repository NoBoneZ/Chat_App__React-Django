from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    safe_methods = ("GET", "PUT")

    def has_object_permission(self, request, view, obj):
        if request.user.id == obj.id and request.method in self.safe_methods:
            return True
        return False


class IsStaff(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.is_staff and request.method == "POST")
