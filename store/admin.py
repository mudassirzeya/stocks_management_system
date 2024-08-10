from django.contrib import admin

# Register your models here.
from .models import Company, UserProfile, Stock, BuyStock, SellStock, Customer, Invoice

admin.site.register(Company)
admin.site.register(UserProfile)
admin.site.register(Stock)
admin.site.register(BuyStock)
admin.site.register(SellStock)
admin.site.register(Customer)
admin.site.register(Invoice)
