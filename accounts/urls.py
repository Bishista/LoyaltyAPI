from django.urls import path
from .views import RegisterView, LoginView, ForgotPasswordView, ResetPasswordView
from .views import EmployeeViewSet
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'employees', EmployeeViewSet, basename='employees')

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('forgot-password/', ForgotPasswordView.as_view()),
    path('reset-password/', ResetPasswordView.as_view()),
]
urlpatterns += router.urls