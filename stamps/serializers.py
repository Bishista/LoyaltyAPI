from rest_framework import serializers
from .models import Stamp, Reward, Redemption

class StampSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stamp
        fields = ['id', 'user', 'restaurant', 'count']

class RewardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reward
        fields = ['id', 'restaurant', 'required_stamps', 'description']

class RedemptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Redemption
        fields = ['id', 'user', 'reward', 'redeemed_at']
