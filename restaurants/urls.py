from django.urls import path
from .views import (
    RestaurantListCreateView, RestaurantDetailView,
    MenuItemListCreateView, MenuItemDetailView,
    ReviewListCreateView, ReviewDetailView
)

urlpatterns = [
    path('', RestaurantListCreateView.as_view(), name='restaurant-list-create'),
    path('<int:pk>/', RestaurantDetailView.as_view(), name='restaurant-detail'),
    path('menu/', MenuItemListCreateView.as_view(), name='menu-list-create'),
    path('menu/<int:pk>/', MenuItemDetailView.as_view(), name='menu-detail'),
    path('reviews/', ReviewListCreateView.as_view(), name='review-list-create'),
    path('reviews/<int:pk>/', ReviewDetailView.as_view(), name='review-detail'),
]
