from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User, Group
from django.db import models
from django.contrib.auth.models import AbstractUser

CATEGORIES = [
    ("gjerdani", "ѓердани"),
    ("obetki", "обетки"),
    ("broshovi", "брошови"),
    ("prsteni", "прстени"),
    ("kosa", "додатоци за во коса"),
    ("alki", "алки"),

]


class Accessory(models.Model):
    name = models.CharField(max_length=40)
    description = models.TextField()
    color = models.CharField(max_length=40)
    quantity = models.IntegerField()
    price = models.IntegerField()
    category = models.CharField(max_length=8, choices=CATEGORIES)
    mainImage = models.URLField(null=True, blank=True)
    secondImage = models.URLField(null=True, blank=True)
    datetime = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.name}"


class ShoppingCart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Shopping Cart of user {self.user.username}"

class Sale(models.Model):
    accessory = models.ForeignKey(Accessory, on_delete=models.CASCADE, null=True, blank=True)
    shoppingCart = models.ForeignKey(ShoppingCart, on_delete=models.CASCADE, null=True, blank=True)
    totalPrice = models.IntegerField(null=True, blank=True)
    numOfPieces = models.IntegerField(null=True, blank=True)


class Payment(models.Model):
    accessory = models.ForeignKey(Accessory, on_delete=models.CASCADE, null=True, blank=True)
    shoppingCart = models.ForeignKey(ShoppingCart, on_delete=models.CASCADE, null=True, blank=True)
    numOfPieces = models.IntegerField(null=True, blank=True)
    successfully_paid = models.BooleanField(default=False, null=True)

    def __str__(self):
        return f"User: {self.shoppingCart.user.username} bought {self.accessory.name} with quantity of: {self.numOfPieces}."

@receiver(post_save, sender=User)
def create_shopping_cart(sender, instance, created, **kwargs):
    if created:
        shopping_cart = ShoppingCart.objects.create(user=instance)
        Sale.objects.create(shoppingCart=shopping_cart, accessory=None, totalPrice=0, numOfPieces=0)


post_save.connect(create_shopping_cart, sender=User)
