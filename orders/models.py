from django.db import models


class Order(models.Model):
    restaurant = models.ForeignKey('restaurant.Restaurant', on_delete=models.CASCADE)
    customer = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    items = models.ManyToManyField('restaurant.MenuItem', through='OrderItem')
    special_instructions = models.TextField(blank=True)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    item = models.ForeignKey('restaurant.MenuItem', on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

class KOT(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    table_number = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
