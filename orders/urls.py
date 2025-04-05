from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OrderViewSet, KOTViewSet

router = DefaultRouter()
router.register(r'orders', OrderViewSet)
router.register(r'kots', KOTViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
