from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RestaurantViewSet, MenuItemViewSet, BookingViewSet, ReviewViewSet, RestaurantDetailViewSet

router = DefaultRouter()
router.register(r'restaurants', RestaurantViewSet)
router.register(r'menu', MenuItemViewSet)
router.register(r'bookings', BookingViewSet)
router.register(r'reviews', ReviewViewSet)
router.register(r'restaurant-details', RestaurantDetailViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
