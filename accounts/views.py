from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .serializers import RegisterSerializer, LoginSerializer, ForgotPasswordSerializer, ResetPasswordSerializer
from .utils import send_otp, verify_otp
from restaurant.permissions import IsAdminUser
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets

class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            send_otp(user.phone, user.email)
            return Response({"message": "Registered successfully. OTP sent."}, status=201)
        return Response(serializer.errors, status=400)

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data)
        return Response(serializer.errors, status=401)

class ForgotPasswordView(APIView):
    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user = User.objects.get(phone=serializer.validated_data['phone'])
                send_otp(user.phone, user.email)
                return Response({"message": "OTP sent to your registered phone and email"})
            except User.DoesNotExist:
                return Response({"error": "User not found"}, status=404)
        return Response(serializer.errors, status=400)

class ResetPasswordView(APIView):
    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            phone = serializer.validated_data['phone']
            otp = serializer.validated_data['otp']
            new_password = serializer.validated_data['new_password']
            if verify_otp(phone, otp):
                try:
                    user = User.objects.get(phone=phone)
                    user.set_password(new_password)
                    user.save()
                    return Response({"message": "Password reset successful"})
                except User.DoesNotExist:
                    return Response({"error": "User not found"}, status=404)
            return Response({"error": "Invalid OTP"}, status=400)
        return Response(serializer.errors, status=400)
    
    
class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = User.objects.filter(role='employee')
    serializer_class = RegisterSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def perform_create(self, serializer):
        serializer.save(role='employee')

    def get_queryset(self):
        return User.objects.filter(role='employee')
