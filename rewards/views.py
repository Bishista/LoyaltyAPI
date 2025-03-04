from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from stamps.models import Stamp
from .models import Reward, Redemption
from django.contrib.auth.models import User

def redeem_reward(request, user_id, reward_id):
    user = get_object_or_404(User, id=user_id)
    reward = get_object_or_404(Reward, id=reward_id)

    # Check total stamps
    stamp_count = Stamp.objects.filter(user=user).count()

    if stamp_count >= reward.required_stamps:
        # Deduct stamps
        Stamp.objects.filter(user=user)[:reward.required_stamps].delete()
        # Create redemption record
        Redemption.objects.create(user=user, reward=reward)
        return JsonResponse({"message": f"Reward '{reward.name}' redeemed!"})
    else:
        return JsonResponse({"error": "Not enough stamps"}, status=400)
