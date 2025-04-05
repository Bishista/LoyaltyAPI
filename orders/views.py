from rest_framework import viewsets
from .models import Order, KOT
from .serializers import OrderSerializer, KOTSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        order = serializer.save()
        # Auto-generate KOT when order is created
        KOT.objects.create(order=order, table_number="TBD")  # Replace "TBD" dynamically if needed

class KOTViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = KOT.objects.all()
    serializer_class = KOTSerializer
    permission_classes = [IsAuthenticated]
