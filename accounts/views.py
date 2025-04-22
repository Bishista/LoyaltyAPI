from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .serializers import RegisterSerializer, LoginSerializer, ForgotPasswordSerializer, ResetPasswordSerializer
from .utils import send_otp, verify_otp
from restaurant.permissions import IsAdminUser
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token



class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            send_otp(user.phone, user.email)
            return Response({"message": "Registered successfully. OTP sent."}, status=201)
        return Response(serializer.errors, status=400)

# class LoginView(APIView):
#     def post(self, request):
#         serializer = LoginSerializer(data=request.data)
#         if serializer.is_valid():
#             return Response(serializer.validated_data)
#         return Response(serializer.errors, status=401)

# class LoginView(APIView):
#     def post(self, request):
#         serializer = LoginSerializer(data=request.data)
#         if serializer.is_valid():
#             user = User.objects.get(id=serializer.validated_data['user_id'])

#             # Generate tokens
#             refresh = RefreshToken.for_user(user)

#             return Response({
#                 "refresh": str(refresh),
#                 "access": str(refresh.access_token),
#                 "user": {
#                     "id": user.id,
#                     "name": user.name,
#                     "role": user.role
#                 }
#             })
#         return Response(serializer.errors, status=401)


# this the one working now
class LoginView(APIView):
    def post(self, request):
        phone = request.data.get('phone')
        password = request.data.get('password')
        print(phone)

        if not phone or not password:
            return Response({'error': 'Phone and password required.'}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=phone, password=password)
        
        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                'message': 'Login successful',
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'user': {
                    'phone': user.phone  # or user.phone if you have a separate phone field
                }
            }, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        # if user is not None:
        #     return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
        # else:
        #     return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)



# User = get_user_model()

# class LoginView(APIView):
#     def post(self, request):
        

#         phone = request.data.get('phone')
#         password = request.data.get('password')

#         if not phone or not password:
#             return Response({'error': 'Phone and password required.'}, status=status.HTTP_400_BAD_REQUEST)

#         user = authenticate(username=phone, password=password)

#         if user is not None:
#             refresh = RefreshToken.for_user(user)
#             return Response({
#                 'message': 'Login successful',
#                 'access': str(refresh.access_token),
#                 'refresh': str(refresh),
#                 'user': {
#                     'phone': user.username,  # or user.phone if different
#                     'username': user.username
#                 }
#             }, status=status.HTTP_200_OK)
#         else:
#             return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


    
    

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
        serializer.save()

    def get_queryset(self):
        return User.objects.all()
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({'detail': 'Employee deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
    

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = RegisterSerializer(request.user)
        return Response(serializer.data)

    def put(self, request):
        serializer = RegisterSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        current_password = request.data.get('current_password')
        new_password = request.data.get('new_password')

        if not user.check_password(current_password):
            return Response({'error': 'Current password is incorrect'}, status=400)

        user.set_password(new_password)
        user.save()
        return Response({'message': 'Password changed successfully'})


