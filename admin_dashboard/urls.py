from django.urls import path
from .views import admin_dashboard, admin_logout

urlpatterns = [
    path('', admin_dashboard, name='admin_dashboard'),
    path('logout/', admin_logout, name='logout'),
]
