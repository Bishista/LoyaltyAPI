from django.db import models

class DigitalLoyaltyCard(models.Model):
    customer = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    background_image = models.ImageField(null=True)
    slot_number = models.IntegerField(default=0)
    slot_image = models.ImageField(null=True)
    is_active = models.BooleanField(default=True)
    name =  models.CharField(max_length=255)
    
    
class Reward(models.Model):
    name =  models.CharField(max_length=255)
    card = models.ForeignKey(DigitalLoyaltyCard, related_name='rewards', on_delete=models.CASCADE)
    stamp_goal = models.IntegerField(default=0) 
    reward_image = models.ImageField(null=True)# stamps needed
    expiration_days = models.IntegerField(default=30)

    def __str__(self):
        return f"Reward from {self.restaurant.name}"


class UserDigitalCard(models.Model):
    customer = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    card = models.ForeignKey(DigitalLoyaltyCard, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer.phone} - {self.card.name}"
    

class StampTransaction(models.Model):
    employee = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    user_card = models.ForeignKey('UserDigitalCard', related_name= 'transactions', on_delete=models.CASCADE)
    stamped = models.BooleanField(default=True)
    is_reward_slot = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"Stamp for {self.employee.phone} on {self.user_card.card.name}"


class CustomerReward(models.Model):
    name = models.CharField(max_length=255)
    customer = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    user_card = models.ForeignKey(StampTransaction, on_delete=models.CASCADE)
    is_claimed = models.BooleanField(default=False)
    reward_img =models.ImageField(null = True)
    assigned_at = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True, null = True)
    

