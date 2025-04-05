from rest_framework import serializers
from .models import User
from django.contrib.auth import authenticate

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name', 'email', 'phone', 'password', 'role']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class LoginSerializer(serializers.Serializer):
    phone = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(phone=data['phone'], password=data['password'])
        if not user:
            raise serializers.ValidationError("Invalid credentials")
        return {'user_id': user.id, 'name': user.name, 'role': user.role}

class ForgotPasswordSerializer(serializers.Serializer):
    phone = serializers.CharField()

class ResetPasswordSerializer(serializers.Serializer):
    phone = serializers.CharField()
    otp = serializers.CharField()
    new_password = serializers.CharField()
