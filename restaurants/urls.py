from django.urls import path
from .views import (
    RestaurantListCreateView, RestaurantDetailView,
    MenuItemListCreateView, MenuItemDetailView,
    ReviewCreateView
)

urlpatterns = [
    path('', RestaurantListCreateView.as_view(), name='restaurant-list'),
    path('<int:pk>/', RestaurantDetailView.as_view(), name='restaurant-detail'),

    # Menu endpoints
    path('menu/', MenuItemListCreateView.as_view(), name='menu-list'),
    path('menu/<int:pk>/', MenuItemDetailView.as_view(), name='menu-detail'),

    # Review endpoint
    path('review/', ReviewCreateView.as_view(), name='review-create'),
]
