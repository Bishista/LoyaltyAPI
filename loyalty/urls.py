from django.urls import path
from .views import *

urlpatterns = [
    path('create-card-with-reward/', CreateCardWithRewardView.as_view(), name='create_card_with_reward'),
    path('card/<int:pk>/', CreateCardWithRewardView.as_view(), name='create_card_with_reward'),
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
    
    path('issue-stamps/', IssueStampedView.as_view(), name='issue-stamp'),
    path('claim-reward/', ClaimRewardView.as_view(), name='claim-reward'),

    path('status/reward-summary/', RewardStatusSummaryView.as_view(), name='reward-status-summary'),
    path('my-reward/', MyRewardsView.as_view(), name='reward-status-summary'),


]
