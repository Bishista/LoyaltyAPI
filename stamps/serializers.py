from rest_framework import serializers
from .models import Stamp, Redemption

class StampSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stamp
        fields = ['id', 'user', 'created_at']  # Removed 'restaurant' (since it doesn’t exist)

class RedemptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Redemption
        fields = ['id', 'user', 'reward', 'redeemed_at']
