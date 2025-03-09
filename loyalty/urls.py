from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LoyaltyProgramViewSet

# Create router and register the viewset
router = DefaultRouter()
router.register(r'loyalty-programs', LoyaltyProgramViewSet, basename='loyalty-program')
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LoyaltyProgramViewSet

# Create router and register the viewset
router = DefaultRouter()
router.register(r'loyalty-programs', LoyaltyProgramViewSet, basename='loyalty-program')

urlpatterns = [
    path('', include(router.urls)),  # Include all CRUD routes
]

urlpatterns = [
    path('', include(router.urls)),  # Include all CRUD routes
]
