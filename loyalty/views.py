from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import *
from .serializers import *
from accounts.models import User
from restaurant.models import Restaurant
from django.utils import timezone
from rest_framework.permissions import IsAuthenticated
from restaurant.permissions import IsAdminUser, IsEmployeeUser, IsSuperUser
from rest_framework import viewsets
from .serializers import (
    RewardSerializer,
    CustomerRewardSerializer,
    UserDigitalCardSerializer,
    StampTransactionSerializer,
)


# class StampAdminViewSet(viewsets.ReadOnlyModelViewSet):
#     queryset = Stamp.objects.all().select_related('customer', 'restaurant')
#     serializer_class = StampSerializer
#     permission_classes = [IsAuthenticated, IsAdminUser]

# class CustomerRewardAdminViewSet(viewsets.ModelViewSet):
#     queryset = CustomerReward.objects.all().select_related('customer', 'reward')
#     serializer_class = CustomerRewardSerializer
#     permission_classes = [IsAuthenticated, IsAdminUser]
    
    
# class IssueStampView(APIView):
#     permission_classes = [permissions.IsAuthenticated]

#     def post(self, request):
#         phone = request.data.get('phone')
#         restaurant_id = request.data.get('restaurant_id')

#         try:
#             customer = User.objects.get(phone=phone, role='customer')
#             restaurant = Restaurant.objects.get(id=restaurant_id)
#         except (User.DoesNotExist, Restaurant.DoesNotExist):
#             return Response({'error': 'Invalid customer or restaurant'}, status=404)

#         stamp = Stamp.objects.create(customer=customer, restaurant=restaurant)
#         self.check_and_assign_reward(customer, restaurant)

#         return Response({'message': 'Stamp issued', 'stamp_id': stamp.id})

#     def check_and_assign_reward(self, customer, restaurant):
#         total_stamps = Stamp.objects.filter(customer=customer, restaurant=restaurant).count()
#         reward_defs = Reward.objects.filter(restaurant=restaurant).order_by('-stamp_goal')

#         for reward in reward_defs:
#             if total_stamps >= reward.stamp_goal:
#                 exists = CustomerReward.objects.filter(customer=customer, reward=reward).exists()
#                 if not exists:
#                     CustomerReward.objects.create(customer=customer, reward=reward)
#                     break

# class CustomerStampsView(APIView):
#     permission_classes = [permissions.IsAuthenticated]

#     def get(self, request):
#         stamps = Stamp.objects.filter(customer=request.user)
#         serializer = StampSerializer(stamps, many=True)
#         return Response(serializer.data)

# class ClaimRewardView(APIView):
#     permission_classes = [permissions.IsAuthenticated]

#     def post(self, request):
#         reward_id = request.data.get('reward_id')
#         try:
#             reward = CustomerReward.objects.get(id=reward_id, customer=request.user, is_claimed=False)
#             reward.is_claimed = True
#             reward.save()
#             return Response({'message': 'Reward claimed successfully'})
#         except CustomerReward.DoesNotExist:
#             return Response({'error': 'No claimable reward found'}, status=404)

# class MyRewardsView(APIView):
#     permission_classes = [permissions.IsAuthenticated]

#     def get(self, request):
#         rewards = CustomerReward.objects.filter(customer=request.user)
#         serializer = CustomerRewardSerializer(rewards, many=True)
#         return Response(serializer.data)


class CreateCardWithRewardView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsEmployeeUser| IsAdminUser| IsSuperUser]

    def post(self, request):
        serializer = DigitalLoyaltyCardCreateSerializer(data=request.data,context={'request': request})
        if serializer.is_valid():
            card = serializer.save()
            return Response({"card": "created successfully."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        cards = DigitalLoyaltyCard.objects.all()
        serializer = DigitalLoyaltyCardListSerializer(cards, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, pk=None):
        card = get_object_or_404(DigitalLoyaltyCard, pk=pk)
        serializer = DigitalLoyaltyCardCreateSerializer(card, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({"card": "updated successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        card = get_object_or_404(DigitalLoyaltyCard, pk=pk)
        card.delete()
        return Response({"card": "deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
    
class IssueStampView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = IssueStampSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Stamp issued successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        """
         View all stamps issued (you can filter later by customer, card, etc.)
        """
        stamps = UserDigitalCard.objects.all().order_by('-date')
        serializer = StampSerializer(stamps, many=True)
        return Response(serializer.data)


class RewardListCreateView(generics.ListCreateAPIView):
    queryset = Reward.objects.all()
    serializer_class = RewardSerializer
    permission_classes = [permissions.IsAuthenticated]


class CustomerRewardListCreateView(generics.ListCreateAPIView):
    queryset = CustomerReward.objects.all()
    serializer_class = CustomerRewardSerializer
    permission_classes = [permissions.IsAuthenticated]


class CustomerRewardDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomerReward.objects.all()
    serializer_class = CustomerRewardSerializer
    permission_classes = [permissions.IsAuthenticated]


class UserDigitalCardListCreateView(generics.ListCreateAPIView):
    queryset = UserDigitalCard.objects.all()
    serializer_class = UserDigitalCardSerializer
    permission_classes = [permissions.IsAuthenticated]


class UserDigitalCardDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserDigitalCard.objects.all()
    serializer_class = UserDigitalCardSerializer
    permission_classes = [permissions.IsAuthenticated]


class StampTransactionListCreateView(generics.ListCreateAPIView):
    queryset = StampTransaction.objects.all()
    serializer_class = StampTransactionSerializer
    permission_classes = [permissions.IsAuthenticated]


class StampTransactionDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = StampTransaction.objects.all()
    serializer_class = StampTransactionSerializer
    permission_classes = [permissions.IsAuthenticated]




class PieRewardView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        # Get the current user
        user = request.user

        # Get the restaurant associated with the user
        restaurant = Restaurant.objects.get(user=user)

        # Get all rewards for the restaurant
        rewards = Reward.objects.filter(restaurant=restaurant)

        # Create a dictionary to hold reward names and their counts
        reward_data = {}
        for reward in rewards:
            reward_data[reward.name] = CustomerReward.objects.filter(reward=reward).count()

        return Response(reward_data, status=status.HTTP_200_OK)