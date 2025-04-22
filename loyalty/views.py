from datetime import datetime
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


class RewardStatusSummaryView(APIView):  
    def get(self, request): 
        claimed = CustomerReward.objects.filter(is_claimed=True).count() 
        not_claimed = CustomerReward.objects.filter(is_claimed=False).count() 
        data = {
            "claimed": claimed , 
            "not_claimed": not_claimed 
        }
        return Response(data, status=status.HTTP_200_OK)
    

class IssueStampedView(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        phone = request.data.get('phone', None)
        stamp =  int(request.data.get('stamp', None))
        card_id = request.data.get('card_id', None)
        digital_card = get_object_or_404(DigitalLoyaltyCard, id = card_id)
        
        customer = get_object_or_404(User, phone=phone)
        loyalty_card_slots = {}
        
        for slot in digital_card.rewards.all():
            slot_info = {
                    'name': slot.name,
                    'slot_image': slot.reward_image,
                }
            loyalty_card_slots[slot.stamp_goal] = slot_info
        
        user_loyalty_cards = UserDigitalCard.objects.filter(customer = customer, card = digital_card,).order_by('-date')
       

        if user_loyalty_cards.exists():
            current_user_loyalty_card = user_loyalty_cards.first()
            total_transactions = current_user_loyalty_card.transactions.count()
            current_transaction_no = total_transactions
            available_slots = digital_card.slot_number - total_transactions
        else:
            current_user_loyalty_card = UserDigitalCard.objects.create(customer=customer, card=digital_card)
            current_transaction_no = 0
            available_slots = digital_card.slot_number

        while stamp > 0:
            if available_slots:
                StampTransaction.objects.create(stamped=True, user_card = current_user_loyalty_card, employee = request.user)
                stamp = stamp - 1
                available_slots = available_slots - 1 
                current_transaction_no = current_transaction_no + 1
                #reward generated
                if current_transaction_no + 1 in loyalty_card_slots:
                    reward_transaction = StampTransaction.objects.create(stamped=False, is_reward_slot = True, user_card = current_user_loyalty_card, employee = request.user )
                    slot_info = loyalty_card_slots[current_transaction_no + 1]
                    name = slot_info['name']
                    slot_image= slot_info['slot_image']
                    CustomerReward.objects.create( customer = customer, name= name, reward_img=slot_image, is_claimed = False, user_card = reward_transaction)
                    current_transaction_no = current_transaction_no + 1
                    available_slots = available_slots - 1 
            else: 
                current_user_loyalty_card = UserDigitalCard.objects.create(customer=customer, card= digital_card)
                print(current_user_loyalty_card)
                current_transaction_no = 0
                available_slots = digital_card.slot_number

        UserDigitalCardSerializer(current_user_loyalty_card).data

        return Response(UserDigitalCardSerializer(current_user_loyalty_card).data, status=status.HTTP_201_CREATED)


class ClaimRewardView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        reward_id = request.data.get('reward_id')
        try:
            reward = CustomerReward.objects.get(id=reward_id, customer=request.user)
            if reward.is_claimed:
                return Response({'message': 'Reward has been already claimed.'})
            reward.is_claimed = True
            reward.assigned_at = datetime.now() 
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
