from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Product(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    price = models.DecimalField(max_digits=15, decimal_places=2)

    def __str__(self):
        return self.title



class CartProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="cart_products")
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return self.product.title

    @property
    def full_price(self):
        return self.product.price * self.quantity



class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="ordered_products")
    quantity = models.IntegerField(default=1)
    title = models.CharField(max_length=50)
    description = models.TextField()
    price = models.DecimalField(max_digits=15, decimal_places=2)
    full_price = models.DecimalField(max_digits=15, decimal_places=2)
    date_ordered = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product} ordered by {self.user}"
