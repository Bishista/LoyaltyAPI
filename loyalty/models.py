from django.db import models

class DigitalLoyaltyCard(models.Model):
    customer = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    # restaurant = models.ForeignKey('restaurant.Restaurant', on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    background_image = models.ImageField(null=True)
    slot_number = models.IntegerField(default=0)
    slot_image = models.ImageField(null=True)
    is_active = models.BooleanField(default=True)
    name =  models.CharField(max_length=255)
    
    


class Reward(models.Model):
    # restaurant = models.ForeignKey('restaurant.Restaurant', on_delete=models.CASCADE)
    # description = models.TextField()
    card = models.ForeignKey(DigitalLoyaltyCard, related_name='rewards', on_delete=models.CASCADE)
    stamp_goal = models.IntegerField(default=0) 
    reward_image = models.ImageField(null=True)# stamps needed
    expiration_days = models.IntegerField(default=30)

    def __str__(self):
        return f"Reward from {self.restaurant.name}"


class CustomerReward(models.Model):
    customer = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    card = models.ForeignKey(DigitalLoyaltyCard, on_delete=models.CASCADE)
    reward = models.ForeignKey(Reward, on_delete=models.CASCADE)
    is_claimed = models.BooleanField(default=False)
    assigned_at = models.DateTimeField(auto_now_add=True)
    


class UserDigitalCard(models.Model):
    customer = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    card = models.ForeignKey(DigitalLoyaltyCard, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer.phone} - {self.card.name}"
    
    


class StampTransaction(models.Model):
    customer = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    user_card = models.ForeignKey('UserDigitalCard', on_delete=models.CASCADE)
    stamp = models.IntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Stamp for {self.customer.phone} on {self.user_card.card.name}"


