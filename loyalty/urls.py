from django.urls import path
from .views import (
  CreateCardWithRewardView,
  IssueStampView,
  RewardListCreateView,
  CustomerRewardListCreateView,
  CustomerRewardDetailView,
  UserDigitalCardListCreateView,
  UserDigitalCardDetailView,
  StampTransactionListCreateView,
  StampTransactionDetailView
  
)

urlpatterns = [
    path('create-card-with-reward/', CreateCardWithRewardView.as_view(), name='create_card_with_reward'),
    path('issue-stamp/', IssueStampView.as_view(), name='issue-stamp'),
    path('rewards/', RewardListCreateView.as_view(), name='reward-list-create'),
    # Customer Rewards
    path('customer-rewards/', CustomerRewardListCreateView.as_view(), name='customer-reward-list-create'),
    path('customer-rewards/<int:pk>/', CustomerRewardDetailView.as_view(), name='customer-reward-detail'),

    # User Digital Cards
    path('user-cards/', UserDigitalCardListCreateView.as_view(), name='user-card-list-create'),
    path('user-cards/<int:pk>/', UserDigitalCardDetailView.as_view(), name='user-card-detail'),

    # Stamp Transactions
    path('stamps/', StampTransactionListCreateView.as_view(), name='stamp-transaction-list-create'),
    path('stamps/<int:pk>/', StampTransactionDetailView.as_view(), name='stamp-transaction-detail'),
    
]
