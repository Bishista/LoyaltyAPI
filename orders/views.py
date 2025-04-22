from rest_framework import viewsets
from .models import Order, KOT, OrderItem
from .serializers import OrderSerializer, KOTSerializer
from rest_framework.permissions import IsAuthenticated
from restaurant.permissions import IsAdminUser, IsSuperUser, IsEmployeeUser
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from django.db.models import Q

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all().order_by('-created_at')
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        try:
            order = serializer.save()
            # Auto-generate KOT when order is created
            # KOT.objects.create(order=order, table_number="TBD")  # Replace "TBD" dynamically if needed
            table_number = self.request.data.get('table_number', 'TBD')  # Get table number from request data
            KOT.objects.create(order=order, table_number=table_number)  # Create KOT with the provided table number
        except Exception as e:
            # Log the error for debugging
            print(f"Error creating order: {str(e)}")
            raise

# class KOTViewSet(viewsets.ReadOnlyModelViewSet):
#     queryset = KOT.objects.all()
#     serializer_class = KOTSerializer
#     permission_classes = [IsAuthenticated]

class KOTViewSet(viewsets.ModelViewSet):  # Changed from ReadOnlyModelViewSet to ModelViewSet
    queryset = KOT.objects.all()
    serializer_class = KOTSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        queryset = KOT.objects.all()
        
        # Filter by table number if provided
        table_number = self.request.query_params.get('table_number', None)
        if table_number:
            queryset = queryset.filter(table_number=table_number)
            
        # If user is admin, they can see all KOTs
        # If user is merchant, they can only see KOTs for their restaurant
        if not user.is_staff and hasattr(user, 'restaurant'):
            queryset = queryset.filter(order__restaurant=user.restaurant)
            
        return queryset
    
    @action(detail=True, methods=['patch'])
    def update_status(self, request, pk=None):
        kot = self.get_object()
        new_status = request.data.get('status') 
        
        if new_status not in [choice[0] for choice in KOT.KOT_STATUS_CHOICES]:
            return Response({"error": "Invalid status"}, status=status.HTTP_400_BAD_REQUEST)
            
        kot.status = new_status
        kot.save()
        
        return Response(KOTSerializer(kot).data)
    
    
    def update (self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        # Check if the status is updated to 'completed'
        if 'status' in request.data and request.data['status'] == 'completed':
            # Perform any additional actions needed when KOT is completed
            pass
        return Response(serializer.data)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    
    
    
    
    
   