from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.http import JsonResponse
from .models import Stamp

def add_stamp(request, user_id):
    user = get_object_or_404(User, id=user_id)
    Stamp.objects.create(user=user)
    return JsonResponse({"message": f"Stamp added for {user.username}"})

def check_stamps(request, user_id):
    user = get_object_or_404(User, id=user_id)
    count = Stamp.objects.filter(user=user).count()
    return JsonResponse({"user": user.username, "stamps": count})
