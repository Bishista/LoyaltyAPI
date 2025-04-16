
from rest_framework import viewsets
from .models import Restaurant, MenuItem, Booking, Review
from .serializers import RestaurantSerializer, MenuItemSerializer, BookingSerializer, ReviewSerializer
from .permissions import IsAdminUser, IsCustomerUser, IsSuperUser, IsEmployeeUser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone

class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class MenuItemViewSet(viewsets.ModelViewSet):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    permission_classes = [IsAuthenticated, IsAdminUser|IsEmployeeUser]

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated,IsCustomerUser|IsAdminUser|IsSuperUser]

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user)

    def list(self, request):
        # Customers only see their bookings
        bookings = Booking.objects.all()
        serializer = self.serializer_class(bookings, many=True)
        return Response(serializer.data)

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated, IsCustomerUser]

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user)
