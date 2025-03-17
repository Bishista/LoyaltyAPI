from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Stamp, Redemption
from .serializers import StampSerializer, RedemptionSerializer
from users.models import CustomUser
from .permissions import IsAdmin, IsRestaurant

class AddStampView(generics.CreateAPIView):
    serializer_class = StampSerializer
    permission_classes = [IsAuthenticated, IsAdmin | IsRestaurant]

    def post(self, request, *args, **kwargs):
        # Expect the phone number in the URL.
        phone_number = kwargs.get("phone_number")
        if not phone_number:
            return Response({"error": "Phone number is required."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = CustomUser.objects.get(phone_number=phone_number)
        except CustomUser.DoesNotExist:
            return Response({"error": "❌ User not found."}, status=status.HTTP_404_NOT_FOUND)
        # Add a stamp for the found user.
        Stamp.objects.create(user=user)
        return Response({
            "message": "✅ Stamp added successfully!",
            "username": user.username,
            "phone_number": user.phone_number,
            "stamps": Stamp.objects.filter(user=user).count(),
        }, status=status.HTTP_201_CREATED)

class CheckStampsView(generics.RetrieveAPIView):
    serializer_class = StampSerializer
    # Uncomment the next line if you require authentication
    # permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        phone_number = kwargs.get("phone_number")
        if phone_number:
            phone_number = phone_number.strip()  # Remove extra spaces
        print("Received phone number:", phone_number)  # Debug output

        if not phone_number:
            return Response({"error": "Phone number is required."}, status=status.HTTP_400_BAD_REQUEST)

        # Perform a case-insensitive lookup (whitespace should be handled now)
        user = CustomUser.objects.filter(phone_number__iexact=phone_number).first()

        if not user:
            return Response({"error": "❌ User not found."}, status=status.HTTP_404_NOT_FOUND)

        stamp_count = Stamp.objects.filter(user=user).count()
        return Response({
            "id": user.id,
            "username": user.username,
            "phone_number": user.phone_number,
            "stamps": stamp_count,
        }, status=status.HTTP_200_OK)
        
class RedeemRewardView(generics.CreateAPIView):
    serializer_class = RedemptionSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        user = request.user
        reward = request.data.get("reward")
        if not reward:
            return Response({"error": "Reward is required!"}, status=status.HTTP_400_BAD_REQUEST)
        Redemption.objects.create(user=user, reward=reward)
        return Response({
            "message": f"✅ {reward} redeemed successfully!",
            "username": user.username,
            "redeemed_at": Redemption.objects.filter(user=user).latest('redeemed_at').redeemed_at
        }, status=status.HTTP_201_CREATED)