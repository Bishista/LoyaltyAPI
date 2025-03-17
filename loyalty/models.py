from django.db import models
from users.models import CustomUser
from restaurants.models import Restaurant  # Import the Restaurant model

class LoyaltyProgram(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    points_required = models.IntegerField()  # Points needed to redeem
    discount_percentage = models.FloatField()  # Discount percentage
    restaurant = models.CharField(max_length=100, default="Default Restaurant")
 # Linked to a restaurant
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # Merchant/admin who created it
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.restaurant.name}"
