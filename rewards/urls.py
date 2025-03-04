from django.urls import path
from .views import redeem_reward

urlpatterns = [
    path('redeem/<int:user_id>/<int:reward_id>/', redeem_reward, name='redeem_reward'),
]
