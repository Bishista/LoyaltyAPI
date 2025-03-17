import random
from django.conf import settings
from twilio.rest import Client
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import CustomUser
from .serializers import RegisterSerializer, LoginSerializer, EmployeeCreateSerializer, UserSerializer
from .permissions import IsAdmin, IsRestaurant, IsUser
from rest_framework.permissions import AllowAny, IsAuthenticated

# 🔹 Function to send OTP via SMS
def send_otp_via_sms(phone_number, otp):
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    message = client.messages.create(
        body=f"Your OTP is: {otp}",
        from_=settings.TWILIO_PHONE_NUMBER,
        to=phone_number
    )
    return message.sid

# 🔹 User Registration with OTP
class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        user = serializer.save()
        otp_code = str(random.randint(100000, 999999))
        user.otp = otp_code
        user.save()
        send_otp_via_sms(user.phone_number, otp_code)

        return Response({
            'message': 'User registered successfully! OTP sent via SMS.',
            'user_id': user.id,
            'role': user.role
        }, status=status.HTTP_201_CREATED)

# 🔹 Login View (JWT Authentication)
class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']
            password = serializer.validated_data['password']

            try:
                user = CustomUser.objects.get(phone_number=phone_number)
            except CustomUser.DoesNotExist:
                return Response({'error': 'User does not exist'}, status=status.HTTP_400_BAD_REQUEST)

            user = authenticate(username=user.username, password=password)

            if user:
                refresh = RefreshToken.for_user(user)
                return Response({
                    'message': 'Login successful',
                    'role': user.role,
                    'user': {
                        'id': user.id,
                        'username': user.username,
                        'email': user.email,
                        'phone_number': user.phone_number,
                        'is_verified': user.is_verified,
                        'role': user.role
                    },
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }, status=status.HTTP_200_OK)

            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 🔹 Admin: List & Create Users
class ManageUsersView(generics.ListCreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdmin]  

    def create(self, request, *args, **kwargs):
        print("🔹 Received Data:", request.data)  # Debugging
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            print(" User Created Successfully!")
            return Response({"message": "User Created Successfully!", "user": serializer.data}, status=status.HTTP_201_CREATED)
        
        print("❌ Error:", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 🔹 Admin: Retrieve, Update, Delete Users
class ManageUserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdmin]

# 🔹 Admin: Create Employee
class CreateEmployeeView(generics.CreateAPIView):
    """Only Admins can create Employees"""
    serializer_class = EmployeeCreateSerializer
    permission_classes = [IsAuthenticated, IsAdmin]

    def perform_create(self, serializer):
        employee = serializer.save(role="restaurant")  #  Automatically set role to restaurant
        print(f" Employee Created: {employee.username} - {employee.role}")
        return Response({'message': 'Employee created successfully!', 'employee_id': employee.id}, status=status.HTTP_201_CREATED)

# 🔹 Admin Dashboard View
class AdminDashboardView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request):
        return Response({"message": "Welcome to the Admin Dashboard!"}, status=status.HTTP_200_OK)

# 🔹 Employee (Restaurant) Dashboard View
class RestaurantDashboardView(APIView):
    permission_classes = [IsAuthenticated, IsRestaurant]

    def get(self, request):
        return Response({"message": "Welcome to the Restaurant Dashboard!"}, status=status.HTTP_200_OK)

# 🔹 User (Customer) Dashboard View
class UserDashboardView(APIView):
    permission_classes = [IsAuthenticated, IsUser]

    def get(self, request):
        return Response({"message": "Welcome to the User Dashboard!"}, status=status.HTTP_200_OK)
