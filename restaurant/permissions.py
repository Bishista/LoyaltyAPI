from rest_framework.permissions import BasePermission

class IsAdminUser(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.role == 'admin'

class IsCustomerUser(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.role == 'customer'

class IsSuperUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_superuser
    

class IsEmployeeUser(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.role == 'employee'
