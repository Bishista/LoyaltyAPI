from rest_framework.permissions import BasePermission

class IsAdmin(BasePermission):
    """ Allow only Admin users"""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'admin'

class IsRestaurant(BasePermission):
    """ Allow only Restaurant employees"""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'restaurant'

class IsUser(BasePermission):
    """ Allow only Customers"""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'user'
