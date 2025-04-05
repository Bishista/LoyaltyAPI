from rest_framework import serializers
from .models import Stamp, Reward, CustomerReward
from accounts.models import User
from restaurant.models import Restaurant

class StampSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stamp
        fields = '__all__'

class RewardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reward
        fields = '__all__'

class CustomerRewardSerializer(serializers.ModelSerializer):
    reward_details = RewardSerializer(source='reward', read_only=True)

    class Meta:
        model = CustomerReward
        fields = ['id', 'customer', 'reward', 'reward_details', 'is_claimed', 'assigned_at']
        read_only_fields = ['assigned_at']
