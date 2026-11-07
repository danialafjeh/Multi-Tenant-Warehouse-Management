from rest_framework.permissions import BasePermission
from api.models import APIKey



class HasValidAPIKey(BasePermission):
    def has_permission(self, request, view):
        return (
            isinstance(request.auth, APIKey)
            and request.auth.is_active
        )
    