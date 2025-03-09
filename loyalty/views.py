from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import LoyaltyProgram
from .serializers import LoyaltyProgramSerializer

class LoyaltyProgramViewSet(viewsets.ModelViewSet):
    """
    API View to perform CRUD operations on Loyalty Program model.
    Only restaurant owners can create programs for their restaurant.
    """
    queryset = LoyaltyProgram.objects.all()
    serializer_class = LoyaltyProgramSerializer
    permission_classes = [IsAuthenticated]  # Require authentication

    def get_queryset(self):
        """Filter loyalty programs by the authenticated merchant's restaurants"""
        user = self.request.user
        if user.is_superuser:
            return LoyaltyProgram.objects.all()  # Admin can see all programs
        return LoyaltyProgram.objects.filter(created_by=user)  # Merchant sees only their programs

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)  # Assign creator
