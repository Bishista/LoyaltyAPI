from django.db import models

class Booking(models.Model):
    user = models.ForeignKey("users.CustomUser", on_delete=models.CASCADE)
    restaurant = models.ForeignKey("restaurants.Restaurant", on_delete=models.CASCADE)
    date = models.DateTimeField()
    status = models.CharField(max_length=20, choices=[("pending", "Pending"), ("confirmed", "Confirmed")])

    def __str__(self):
        return f"Booking {self.id} - {self.user.username} at {self.restaurant.name}"
