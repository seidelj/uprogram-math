from rest_framework.permissions import BasePermission

class IsSSL(BasePermission):

    def has_permission(self, request, view):
        return request.is_secure()

