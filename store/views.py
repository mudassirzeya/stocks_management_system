import json
from django.core import serializers
from django.http import JsonResponse

from django.shortcuts import render, redirect
from .forms import CompanyForm, RegisterForm, InternalUserForm, StockForm, BuyStockForm, SellStockForm, UserprofileForm, UserForm
from .models import UserProfile, Stock, BuyStock, SellStock
from django.contrib.auth import authenticate, login, logout
# from django.contrib.auth.models import User
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail
from .password import PasswordSet
# Create your views here.


def registration(request):
    form1 = CompanyForm()
    form2 = RegisterForm()
    if request.method == 'POST':
        form2 = RegisterForm(request.POST)
        print("form2: ", form2)
        form1 = CompanyForm(request.POST)
        print("form1: ", form1)
        username = request.POST.get('email')
        print("username: ", username)
        if form2.is_valid():
            print("form2 valid")
            newuser_obj = form2.save(commit=False)
            print("form2: ", newuser_obj)
            newuser_obj.username = username
            newuser_obj.save()
            if form1.is_valid():
                print("form1 valid")
                company_obj = form1.save(commit=False)
                company_obj.super_user = newuser_obj
                company_obj.save()
                UserProfile.objects.create(
                    user=newuser_obj,
                    company=company_obj,
                )
                return redirect('admin_page')
        else:
            print("form2 not valid")

    context = {"form1": form1, "form2": form2}
    return render(request, 'signup.html', context)


def loginuser(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        # user = request.user

        if user is not None:
            login(request, user)
            userProfile = UserProfile.objects.get(user=request.user)
            company_name = userProfile.company
            superuser = company_name.super_user

            print("request.user: ", request.user)
            print("superuser:", superuser)
            if request.user == superuser:
                print("admin page")
                return redirect('admin_page')
            else:
                print("user page")
                return redirect('user')
        else:
            messages.info(request, 'Username or Password is in correct')
    context = {}
    return render(request, 'login.html', context)
    context = {}
    return render(request, 'login.html', context)


def logoutuser(request):
    logout(request)
    return redirect('login')


def adminpage(request):
    form = InternalUserForm()
    loggedin_user = UserProfile.objects.get(user=request.user)
    mycompany = UserProfile.objects.get(user=request.user).company
    myuser = UserProfile.objects.filter(
        company=mycompany
    )

    all_inventory = Stock.objects.filter(user=request.user)

    total = myuser.count()
    total_inventory = all_inventory.count()

    print(request.user.company.company_name)

    context = {"form": form, "total": total,
               "all": all_inventory, "total_inventory": total_inventory,
               "loggedin_user": loggedin_user}
    return render(request, 'admin.html', context)


def userpage(request):
    loggedin_user = UserProfile.objects.get(user=request.user)
    sell = SellStock.objects.filter(user=request.user)
    buy = BuyStock.objects.filter(user=request.user)
    total_sell = sell.count()
    total_buy = buy.count()
    context = {"total_sell": total_sell,
               "total_buy": total_buy, "loggedin_user": loggedin_user}
    return render(request, 'user.html', context)


def add_new_user(request):
    user = request.user
    userProfile = UserProfile.objects.get(user=user)
    company_name = userProfile.company
    form = InternalUserForm()
    if request.method == 'POST':
        form = InternalUserForm(request.POST)
        if form.is_valid():
            email = request.POST.get('email')
            print("email: ", email)
            passcode = PasswordSet()
            print("password: ", passcode)
            newuser = form.save(commit=False)
            newuser.set_password(passcode)
            newuser.username = email
            newuser.save()
            UserProfile.objects.create(
                user=newuser,
                company=company_name,
            )
            subject = f'welcome to {company_name}'
            message = f'Hi {newuser.first_name}, you have successfully registered in our company. your Username is {newuser.username} & your Password is {passcode}'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [newuser.email, ]
            send_mail(subject, message, email_from, recipient_list)
            return redirect('admin_page')

    context = {"form": form}
    return render(request, 'admin.html', context)


def userprofile(request):
    loggedin_user = UserProfile.objects.get(user=request.user)
    user = request.user
    userprofile = UserProfile.objects.get(user=user)
    form = UserprofileForm(instance=userprofile)
    form2 = UserForm(instance=user)
    if request.method == 'POST':
        print("request.POST: ", request.POST)
        form = UserprofileForm(
            request.POST, request.FILES, instance=userprofile)
        form2 = UserForm(
            request.POST, request.FILES, instance=user)

        if form.is_valid() and form2.is_valid():
            print("form valid")
            form.save()
            form2.save()
        else:
            print("form not valid")
        return redirect('user_profile')
    context = {'form': form, "form2": form2, "loggedin_user": loggedin_user}
    return render(request, 'profile.html', context)


def myusers(request):
    mycompany = UserProfile.objects.get(user=request.user).company
    myuser = UserProfile.objects.filter(
        company=mycompany
    )
    total = myuser.count()
    context = {"myuser": myuser, "total": total}
    return render(request, 'myuser.html', context)


def add_new_inventory(request):
    form = StockForm()
    if request.method == 'POST':
        form = StockForm(request.POST)
        if form.is_valid():
            stock = form.save(commit=False)
            stock.user = request.user
            stock.save()
            print("valid form")
            context = {"form": form, "msg": "Item Has Been Added"}
            return render(request, 'add_stock.html', context)
    print("in valid form")
    context = {"form": form}
    return render(request, 'add_stock.html', context)


def buy_inventory(request):
    form = BuyStockForm()
    userProfile = UserProfile.objects.get(user=request.user)
    company_name = userProfile.company
    superuser = company_name.super_user
    form.fields['buy_inventory'].queryset = Stock.objects.filter(
        user=superuser)
    if request.method == 'POST':
        form = BuyStockForm(request.POST)
        get_inventory = request.POST.get('buy_inventory')
        get_quantity = request.POST.get('quantity')
        print("get_inventory: ", get_inventory)
        if form.is_valid():
            buy = form.save(commit=False)
            buy.user = request.user
            buy.save()

            stock_inventory = Stock.objects.get(id=get_inventory)
            print("stock: ", stock_inventory)
            final = stock_inventory.quantity + int(get_quantity)
            print("final: ", final)
            stock_inventory.quantity = final
            stock_inventory.save()
            return redirect('buy_stock')
    mycompany = UserProfile.objects.get(user=request.user).company
    myuser = UserProfile.objects.filter(
        company=mycompany
    )

    all_buy = []
    for my in myuser:
        sell = BuyStock.objects.filter(user=my.user)
        all_buy.append(sell)
    print("my sell", all_buy)

    context = {"form": form, "all_buy": all_buy}
    return render(request, 'buy_stock.html', context)


def sell_inventory(request):
    # form = SellStockForm()
    userProfile = UserProfile.objects.get(user=request.user)
    company_name = userProfile.company
    superuser = company_name.super_user
    inventory = Stock.objects.filter(user=superuser)
    # form.fields['sell_inventory'].queryset = Stock.objects.filter(
    #     user=superuser)
    if request.method == 'POST':
        # form = SellStockForm(request.POST)
        get_inventory = request.POST.get('sell_inventory')
        print("product", get_inventory)
        get_quantity = request.POST.get('quantity')
        unit_price = Stock.objects.filter(sell_inventory=get_inventory)
        total_price = int(unit_price)*int(get_quantity)
        sell = SellStock.objects.create(
            user=request.user,
            sell_inventory=get_inventory,
            quantity=get_quantity,
            total_invoice=total_price,
        )

        sell.save()

        stock_inventory = Stock.objects.get(id=get_inventory)
        print("stock: ", stock_inventory)
        final = stock_inventory.quantity - int(get_quantity)
        print("final: ", final)
        stock_inventory.quantity = final
        stock_inventory.save()
        context = {"unit": unit_price}
        return render(request, 'sell_stock.html', context)
    mycompany = UserProfile.objects.get(user=request.user).company
    myuser = UserProfile.objects.filter(
        company=mycompany
    )

    all_sell = []
    for my in myuser:
        sell = SellStock.objects.filter(user=my.user)
        all_sell.append(sell)

    json_data = serializers.serialize('json', inventory)
    for im in json_data:
        print("json: ", im)

    print("data: ", json_data)

    context = {"all_sell": all_sell,
               "inventory": inventory, "json_data": json_data}
    return render(request, 'sell_stock.html', context)


# def get_product_price(request):
#     print("Hello")
#     if request.method == 'POST':
#         data = json.loads(request.body)
#         print("data: ",  data)
#         product_id = data['produxt_id']
#         stock_x = Stock.objects.get(id=product_id)
#         print("stock: ", stock_x)

#         # stock = serializers.serialize('json', stock_x)
#         # return HttpResponse(stock, content_type="application/json")
#         return JsonResponse({"price": stock_x.current_price})
