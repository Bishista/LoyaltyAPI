from django.db import models
from django.conf import settings 

class Reward(models.Model):
    name = models.CharField(max_length=100)
    required_stamps = models.IntegerField()
    description = models.TextField()

    def __str__(self):
        return f"{self.name} - Requires {self.required_stamps} stamps"

class Redemption(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="rewards_redemptions")
    reward = models.ForeignKey(Reward, on_delete=models.CASCADE)
    redeemed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} redeemed {self.reward.name} on {self.redeemed_at}"
