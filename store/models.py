from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Company(models.Model):
    super_user = models.OneToOneField(
        User, null=True, blank=True, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=200)
    phone = models.CharField(max_length=100, blank=True)
    profile_pic = models.ImageField(
        default="profile1.jpg", null=True, blank=True)

    def __str__(self):
        return self.company_name


class UserProfile(models.Model):
    user = models.OneToOneField(
        User, null=True, blank=True, on_delete=models.CASCADE
    )
    company = models.ForeignKey(
        Company, null=True, blank=True, on_delete=models.CASCADE)
    profile_pic = models.ImageField(
        default="profile1.jpg", null=True, blank=True)
    phone = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return str(self.user)


class Stock(models.Model):
    user = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.CASCADE
    )
    inventory = models.CharField(max_length=100, blank=True)
    current_price = models.BigIntegerField(
        blank=True, null=True)
    quantity = models.PositiveIntegerField(default=0)
    event_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.inventory:
            return str(self.inventory) + '-' + str(self.id)
        return self.id


class BuyStock(models.Model):
    user = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.CASCADE
    )
    buy_inventory = models.ForeignKey(
        Stock, null=True, blank=True, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(blank=True)
    total_invoice = models.BigIntegerField(
        null=True, blank=True)
    event_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.buy_inventory:
            return str(self.buy_inventory)
        return self.id


class SellStock(models.Model):
    user = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.CASCADE
    )
    sell_inventory = models.ForeignKey(
        Stock, blank=True, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(null=True, blank=True)
    total_invoice = models.BigIntegerField(
        null=True, blank=True)
    event_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.sell_inventory:
            return str(self.sell_inventory)
        return self.id
