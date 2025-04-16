from django.db import models


class Order(models.Model):
    restaurant_id = models.ForeignKey('restaurant.Restaurant', on_delete=models.CASCADE)
    customer_id = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    items = models.ManyToManyField('restaurant.MenuItem', through='OrderItem')
    special_instructions = models.TextField(blank=True)
    
    ORDER_STATUS_CHOICES = [
    ('pending', 'Pending'),
    ('kitchen', 'In Kitchen'),
    ('served', 'Served'),
]

    status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='pending')


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    item = models.ForeignKey('restaurant.MenuItem', on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

# class KOT(models.Model):
#     order = models.OneToOneField(Order, on_delete=models.CASCADE)
#     table_number = models.CharField(max_length=10)
#     created_at = models.DateTimeField(auto_now_add=True)

class KOT(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    table_number = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    
    KOT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
    ]
    status = models.CharField(max_length=20, choices=KOT_STATUS_CHOICES, default='pending')