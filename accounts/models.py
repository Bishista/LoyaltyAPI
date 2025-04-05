# accounts/models.py
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class UserManager(BaseUserManager):
    def create_user(self, phone, name, email, password=None, role='customer'):
        if not phone:
            raise ValueError("Users must have a phone number")
        user = self.model(phone=phone, name=name, email=email, role=role)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, name, email, password):
        return self.create_user(phone, name, email, password, role='admin')

class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ('customer', 'Customer'),
        ('employee', 'Employee'),
        ('admin', 'Admin'),
    )
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, unique=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['email', 'name']

    objects = UserManager()

    def __str__(self):
        return f"{self.name} ({self.role})"
