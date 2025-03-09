from rest_framework import serializers
from .models import LoyaltyProgram

class LoyaltyProgramSerializer(serializers.ModelSerializer):
    restaurant_id = serializers.IntegerField(write_only=True)  # Accept restaurant ID in request

    class Meta:
        model = LoyaltyProgram
        fields = ['id', 'name', 'description', 'points_required', 'discount_percentage', 'restaurant_id', 'created_by', 'created_at', 'updated_at']
        read_only_fields = ['created_by', 'created_at', 'updated_at']

    def create(self, validated_data):
        restaurant_id = validated_data.pop('restaurant_id')
        validated_data['restaurant'] = Restaurant.objects.get(id=restaurant_id)  # Assign restaurant
        return super().create(validated_data)
