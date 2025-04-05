from django.db import models

class Stamp(models.Model):
    customer = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    restaurant = models.ForeignKey('restaurant.Restaurant', on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)


class Reward(models.Model):
    restaurant = models.ForeignKey('restaurant.Restaurant', on_delete=models.CASCADE)
    description = models.TextField()
    stamp_goal = models.IntegerField(default=5)  # stamps needed
    expiration_days = models.IntegerField(default=30)

    def __str__(self):
        return f"Reward from {self.restaurant.name}"


class CustomerReward(models.Model):
    customer = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    reward = models.ForeignKey(Reward, on_delete=models.CASCADE)
    is_claimed = models.BooleanField(default=False)
    assigned_at = models.DateTimeField(auto_now_add=True)
