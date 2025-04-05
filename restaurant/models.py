from django.db import models
from django.utils import timezone
from datetime import timedelta

class Restaurant(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField()
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=20)
    created_by = models.ForeignKey('accounts.User', on_delete=models.CASCADE, limit_choices_to={'role': 'admin'})

    def __str__(self):
        return self.name
    
class MenuItem(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='menu_items')
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"{self.name} - {self.restaurant.name}"


class Booking(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    customer = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    booking_time = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.expires_at:
            self.expires_at = timezone.now() + timedelta(minutes=30)
        super().save(*args, **kwargs)
        


class Review(models.Model):
    customer = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    text = models.TextField()
    rating = models.IntegerField()

    def __str__(self):
        return f"{self.customer.name} on {self.restaurant.name}"


