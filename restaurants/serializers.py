from rest_framework import serializers
from .models import Restaurant, MenuItem, Review
from users.models import CustomUser

class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = '__all__'

class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)  # show username

    class Meta:
        model = Review
        fields = ['id', 'user', 'rating', 'comment', 'created_at']

class RestaurantSerializer(serializers.ModelSerializer):
    menu = MenuItemSerializer(many=True, read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = Restaurant
        fields = ['id', 'name', 'phone_number', 'address', 'details', 'menu', 'reviews']
