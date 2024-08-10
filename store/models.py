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
    last_invoice = models.PositiveBigIntegerField(
        default=0, blank=True)

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
        return str(self.user.username)


class Stock(models.Model):
    user = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.CASCADE
    )
    inventory = models.CharField(max_length=100, blank=True)
    current_price = models.BigIntegerField(
        blank=True, null=True)
    event_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.inventory:
            return str(self.inventory) + '-' + str(self.id)


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


class SellStock(models.Model):
    user = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.CASCADE
    )
    sell_inventory = models.CharField(
        max_length=100, blank=True)
    quantity = models.PositiveIntegerField(null=True, blank=True)
    selling_price = models.BigIntegerField(
        null=True, blank=True)
    invoiceid = models.PositiveBigIntegerField(null=True, blank=True)
    event_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.sell_inventory:
            return str(self.sell_inventory)


class Invoice(models.Model):
    user = models.ForeignKey(
        Company, null=True, blank=True, on_delete=models.CASCADE
    )
    staff = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.CASCADE
    )
    invoice_number = models.CharField(
        max_length=100, blank=True)
    customer_id = models.PositiveIntegerField(null=True, blank=True)
    invoice_date = models.CharField(max_length=10,
                                    null=True, blank=True)
    due_date = models.CharField(max_length=10,
                                null=True, blank=True)
    discount = models.PositiveBigIntegerField(null=True, blank=True)
    total_bill = models.PositiveBigIntegerField(null=True, blank=True)
    event_date = models.DateTimeField(auto_now_add=True)


class Customer(models.Model):
    user = models.ForeignKey(
        Company, null=True, blank=True, on_delete=models.CASCADE
    )

    name = models.CharField(
        max_length=100, blank=True)
    phone = models.CharField(
        max_length=100, blank=True)
    city = models.CharField(
        max_length=100, blank=True)
    event_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.name:
            return str(self.name)
