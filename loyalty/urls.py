from django.urls import path
from .views import IssueStampView, CustomerStampsView, ClaimRewardView, MyRewardsView

urlpatterns = [
    path('issue-stamp/', IssueStampView.as_view()),
    path('my-stamps/', CustomerStampsView.as_view()),
    path('my-rewards/', MyRewardsView.as_view()),
    path('claim-reward/', ClaimRewardView.as_view()),
]
