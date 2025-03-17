from django.urls import path
from .views import (
    RegisterView, LoginView, AdminDashboardView, RestaurantDashboardView, 
    UserDashboardView, ManageUsersView, ManageUserDetailView, CreateEmployeeView
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('admin-dashboard/', AdminDashboardView.as_view(), name='admin-dashboard'),
    path('restaurant-dashboard/', RestaurantDashboardView.as_view(), name='restaurant-dashboard'),
    path('user-dashboard/', UserDashboardView.as_view(), name='user-dashboard'),
    path('manage-users/', ManageUsersView.as_view(), name='manage-users'),
    path('manage-users/<int:pk>/', ManageUserDetailView.as_view(), name='manage-user-detail'),
    path('create-employee/', CreateEmployeeView.as_view(), name='create-employee'),
]
