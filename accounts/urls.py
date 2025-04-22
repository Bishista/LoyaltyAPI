from django.urls import path
from .views import RegisterView, LoginView, ForgotPasswordView, ResetPasswordView, UserProfileView, ChangePasswordView
from .views import EmployeeViewSet
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'employees', EmployeeViewSet, basename='employees')

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('forgot-password/', ForgotPasswordView.as_view()),
    path('reset-password/', ResetPasswordView.as_view()),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
]
urlpatterns += router.urls