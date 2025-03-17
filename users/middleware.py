from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect
from django.urls import reverse

class RoleBasedAccessMiddleware(MiddlewareMixin):
    """Middleware to restrict page access based on roles"""

    def process_request(self, request):
        if request.user.is_authenticated:
            if request.user.role == "admin" and request.path.startswith("/restaurant/"):
                return redirect(reverse("admin-dashboard"))
            elif request.user.role == "restaurant" and request.path.startswith("/admin/"):
                return redirect(reverse("restaurant-dashboard"))
