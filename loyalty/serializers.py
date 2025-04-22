from rest_framework import serializers
from .models import *
from accounts.models import User
from restaurant.models import Restaurant



class RewardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reward
        exclude = ['card']


class DigitalLoyaltyCardCreateSerializer(serializers.ModelSerializer):
    reward = RewardSerializer(required=True)

    class Meta:
        model = DigitalLoyaltyCard
        fields = ['id', 'customer', 'background_image', 'slot_number', 'slot_image', 'is_active', 'name', 'reward']
        read_only_fields = ['customer', 'date', 'is_active']

    def create(self, validated_data):
        reward_data = validated_data.pop('reward')
        customer = self.context['request'].user 
        card = DigitalLoyaltyCard.objects.create(customer=customer, **validated_data)
        Reward.objects.create(card=card, **reward_data)
        return card


class DigitalLoyaltyCardListSerializer(serializers.ModelSerializer):
    rewards = RewardSerializer(many=True, read_only=True)  # use related_name='rewards' in Reward model

    class Meta:
        model = DigitalLoyaltyCard
        fields = '__all__'


class CustomerRewardSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerReward
        fields = '__all__'


class StampTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = StampTransaction
        fields = '__all__'
        read_only_fields = ['date']
        
class UserDigitalCardSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(source='customer.full_name', read_only=True)
    card = DigitalLoyaltyCardListSerializer(read_only=True) 
    transactions = StampTransactionSerializer(many=True)

    class Meta:
        model = UserDigitalCard
        fields = ['id', 'customer', 'customer_name', 'card', 'date','transactions']
        read_only_fields = ['date']

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['customer'] = instance.customer.name
        return rep

