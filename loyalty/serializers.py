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
    reward_details = RewardSerializer(source='reward', read_only=True)

    class Meta:
        model = CustomerReward
        fields = ['id', 'customer', 'reward', 'reward_details', 'is_claimed', 'assigned_at']
        read_only_fields = ['assigned_at']




class IssueStampSerializer(serializers.Serializer):
    phone = serializers.CharField()
    card_id = serializers.IntegerField()
    stamp = serializers.IntegerField() 

    def validate(self, data):
        try:
            customer = User.objects.get(phone=data['phone'])
        except User.DoesNotExist:
            raise serializers.ValidationError("Customer not found.")

        try:
            card = DigitalLoyaltyCard.objects.get(id=data['card_id'])
        except DigitalLoyaltyCard.DoesNotExist:
            raise serializers.ValidationError("Loyalty card not found.")

        # if not customer.is_customer:
        #     raise serializers.ValidationError("User is not a customer.")

        # Get or create an active user-card
        user_card, created = UserDigitalCard.objects.get_or_create(
            customer=customer, card=card
        )

        data['customer'] = customer
        data['card'] = card
        data['user_card'] = user_card
        return data

    def create(self, validated_data):
        customer = validated_data['customer']
        card = validated_data['card']
        user_card = validated_data['user_card']
        stamp = validated_data['stamp']

        # Log the stamp
        StampTransaction.objects.create(customer=customer, user_card=user_card, stamp=stamp)

        # Count how many stamps exist for this user_card
        stamp_count = StampTransaction.objects.filter(user_card=user_card).count()

        # Check if reward condition met
        if stamp_count >= card.slot_number:
            try:
                reward = Reward.objects.get(card=card)
                CustomerReward.objects.create(
                    customer=customer,
                    card=card,
                    reward=reward,
                    is_claimed=False
                )
            except Reward.DoesNotExist:
                pass  # No reward for this card

            # Create a new UserDigitalCard for new round
            UserDigitalCard.objects.create(customer=customer, card=card)

        return {"message": "Stamp issued"}

        
class StampSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(source='customer.name', read_only=True)
    card_name = serializers.CharField(source='card.name', read_only=True)

    class Meta:
        model = UserDigitalCard
        fields = ['id', 'customer', 'customer_name', 'card', 'card_name', 'date']
        
class UserDigitalCardSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(source='customer.full_name', read_only=True)  # optional
    # card_name = serializers.CharField(source='card.name', read_only=True)  # optional
    card = DigitalLoyaltyCardListSerializer(read_only=True)  # optional
    class Meta:
        model = UserDigitalCard
        fields = ['id', 'customer', 'customer_name', 'card', 'date']
        read_only_fields = ['date']


class StampTransactionSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(source='customer.full_name', read_only=True)
    card_name = serializers.CharField(source='user_card.card.name', read_only=True)

    class Meta:
        model = StampTransaction
        fields = ['id', 'customer', 'customer_name', 'user_card', 'card_name', 'stamp', 'date']
        read_only_fields = ['date']