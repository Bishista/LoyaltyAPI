from django.urls import path, include
from .views import AddStampView, CheckStampsView, RedeemRewardView

urlpatterns = [
    
    path('add_stamp/<str:phone_number>/', AddStampView.as_view(), name='add-stamp'),
    path('check_stamps/<str:phone_number>/', CheckStampsView.as_view(), name='check-stamps'),
    path('redeem/', RedeemRewardView.as_view(), name='redeem-reward'),
]