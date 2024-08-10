from django.forms import ModelForm
from .models import Company, Stock, BuyStock, SellStock, UserProfile, Customer
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class CompanyForm(ModelForm):
    class Meta:
        model = Company
        fields = ['company_name']


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name',
                  'email', 'password1', 'password2')


class InternalUserForm(ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class StockForm(ModelForm):
    class Meta:
        model = Stock
        fields = ('inventory', 'current_price')


class BuyStockForm(ModelForm):
    class Meta:
        model = BuyStock
        fields = ('buy_inventory', 'quantity', 'total_invoice')


class SellStockForm(ModelForm):
    class Meta:
        model = SellStock
        fields = ('sell_inventory', 'quantity', 'selling_price')


class UserprofileForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ('phone', 'profile_pic')


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name',
                  'email')


class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = ('name', 'phone', 'city')
