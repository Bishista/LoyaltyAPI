from rest_framework import viewsets
from .models import Merchant
from .serializers import MerchantSerializer
from rest_framework.permissions import IsAuthenticated

class MerchantViewSet(viewsets.ModelViewSet):
    """
    API View to perform CRUD operations on Merchant model.
    """
    queryset = Merchant.objects.all()
    serializer_class = MerchantSerializer
    permission_classes = [IsAuthenticated]  # Requires authentication to access API
