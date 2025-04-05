from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Stamp, Reward, CustomerReward
from .serializers import StampSerializer, CustomerRewardSerializer
from accounts.models import User
from restaurant.models import Restaurant
from django.utils import timezone

class IssueStampView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        phone = request.data.get('phone')
        restaurant_id = request.data.get('restaurant_id')

        try:
            customer = User.objects.get(phone=phone, role='customer')
            restaurant = Restaurant.objects.get(id=restaurant_id)
        except (User.DoesNotExist, Restaurant.DoesNotExist):
            return Response({'error': 'Invalid customer or restaurant'}, status=404)

        stamp = Stamp.objects.create(customer=customer, restaurant=restaurant)
        self.check_and_assign_reward(customer, restaurant)

        return Response({'message': 'Stamp issued', 'stamp_id': stamp.id})

    def check_and_assign_reward(self, customer, restaurant):
        total_stamps = Stamp.objects.filter(customer=customer, restaurant=restaurant).count()
        reward_defs = Reward.objects.filter(restaurant=restaurant).order_by('-stamp_goal')

        for reward in reward_defs:
            if total_stamps >= reward.stamp_goal:
                exists = CustomerReward.objects.filter(customer=customer, reward=reward).exists()
                if not exists:
                    CustomerReward.objects.create(customer=customer, reward=reward)
                    break

class CustomerStampsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        stamps = Stamp.objects.filter(customer=request.user)
        serializer = StampSerializer(stamps, many=True)
        return Response(serializer.data)

class ClaimRewardView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        reward_id = request.data.get('reward_id')
        try:
            reward = CustomerReward.objects.get(id=reward_id, customer=request.user, is_claimed=False)
            reward.is_claimed = True
            reward.save()
            return Response({'message': 'Reward claimed successfully'})
        except CustomerReward.DoesNotExist:
            return Response({'error': 'No claimable reward found'}, status=404)

class MyRewardsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        rewards = CustomerReward.objects.filter(customer=request.user)
        serializer = CustomerRewardSerializer(rewards, many=True)
        return Response(serializer.data)
