from django.db import models
from django.contrib.auth.models import User
from product.models import Product, Variation
from django.utils import timezone


# Create your models here.
class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=100)
    payment_method = models.CharField(max_length=100)
    amount_paid = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.payment_id


class Order(models.Model):
    STATUS = (
        ("New", "New"),
        ("Accepted", "Accepted"),
        ("Cancelled", "Cancelled"),
        ("Delivered", "Delivered"),
        ("In Return", "In Return"),
        ("Refunded", "Refunded"),
        ("Completed", "Completed")
    )
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    payment = models.ForeignKey(
        Payment, on_delete=models.SET_NULL, null=True, blank=True
    )
    order_id = models.CharField(max_length=255, null=True)
    phone = models.IntegerField()
    address_1 = models.CharField(max_length=50)
    address_2 = models.CharField(max_length=50, blank=True)
    state = models.CharField(max_length=25)
    city = models.CharField(max_length=20)
    zip = models.IntegerField(null=True)
    note = models.TextField(blank=True)
    total = models.FloatField()
    gift_charges = models.FloatField(null=True)
    tax = models.FloatField()
    grand_total = models.FloatField(null=True)
    status = models.CharField(max_length=20, choices=STATUS, default="New")
    ip = models.CharField(max_length=20, blank=True)
    is_ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    awb = models.CharField(max_length=255, null=True, blank=True)

    def email(self):
        return self.user.email

    def __str__(self):
        return str(self.user)


class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    payment = models.ForeignKey(
        Payment, on_delete=models.SET_NULL, blank=True, null=True
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variations = models.ManyToManyField(Variation, blank=True)
    quantity = models.IntegerField()
    ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def subtotal(self):
        return self.product.price * self.quantity

    def __str__(self):
        return self.product.name
