from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    is_shop_owner = models.BooleanField(default=False)
    
    def __str__(self):
        return self.username
    
class Discount(models.Model):
    price = models.DecimalField(max_digits=10, decimal_places=2) 
    quantity = models.IntegerField()  
    
    def __str__(self):
        return f"{self.quantity} items for {self.price} "
    
class Item(models.Model):
    name = models.CharField(max_length=100, unique=True )
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discounts = models.ManyToManyField(Discount, related_name='items')

    def __str__(self):
        return self.name