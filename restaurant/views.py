
from rest_framework import viewsets
from yaml import serialize
from .models import Restaurant, MenuItem, Booking, Review, RestaurantDetail
from .serializers import RestaurantSerializer, MenuItemSerializer, BookingSerializer, ReviewSerializer, RestaurantDetailSerializer
from .permissions import IsAdminUser, IsCustomerUser, IsSuperUser, IsEmployeeUser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from restaurant.models import Restaurant

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
    permission_classes = [IsAuthenticated,IsCustomerUser|IsAdminUser|IsSuperUser|IsEmployeeUser]

    # def perform_create(self, serializer):
    #     serializer.save(customer=self.request.user)
    # made chaneges to this function to add restaurant id to the bookind as it was asking for it in the serializer
    def perform_create(self, serializer):
        resturantTest = Restaurant.objects.first()
        restaurant = Restaurant.objects.get(id=1)  # 👈 Hardcoded for now
        serializer.save(customer=self.request.user, restaurant=restaurant)

    def list(self, request):
        # Customers only see their bookings
        bookings = Booking.objects.all()
        serializer = self.serializer_class(bookings, many=True)
        return Response(serializer.data)

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated, IsCustomerUser|IsAdminUser|IsSuperUser]

    def perform_create(self, serializer):
        pass  # Add implementation here if needed

class RestaurantDetailViewSet(viewsets.ModelViewSet):
    queryset = RestaurantDetail.objects.all()
    serializer_class = RestaurantDetailSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Auto-assign restaurant based on logged-in user’s created restaurant
        try:
            restaurant = self.request.user.restaurant
        except Restaurant.DoesNotExist:
            restaurant = Restaurant.objects.get(created_by=self.request.user)
        serializer.save(restaurant=restaurant)

    def get_queryset(self):
        user = self.request.user
        if user.role in ['admin', 'employee']:
            try:
                return RestaurantDetail.objects.filter(restaurant=user.restaurant)
            except Restaurant.DoesNotExist:
                return RestaurantDetail.objects.filter(restaurant__created_by=user)
        return RestaurantDetail.objects.all()  # for customer/public access queryset = RestaurantDetail.objects.all()
    serializer_class = RestaurantDetailSerializer
    permission_classes = [IsAuthenticated]

    # def perform_create(self, serializer):
    #     serializer.save()


   

