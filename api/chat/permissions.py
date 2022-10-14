from rest_framework.permissions import BasePermission


class IsSender(BasePermission):
    safe_method = ["GET", "DELETE"]

    def has_object_permission(self, request, view, obj):
        return bool(request.user.id == obj.sender_id and request.method in self.safe_method)


class PostOnly(BasePermission):
    def has_permission(self, request, view):
        return bool(request.method not in IsSender.safe_method)


class IsStarterOrIsSecondParty(BasePermission):

    def has_object_permission(self, request, view, obj):
        return bool(request.user.id == (obj.starter_id or obj.second_party_id) and request.method == "GET")
