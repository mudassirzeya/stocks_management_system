import json
from django.core import serializers
from django.http import JsonResponse
from django.forms import inlineformset_factory
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import CompanyForm, RegisterForm, InternalUserForm, StockForm, BuyStockForm, SellStockForm, UserprofileForm, UserForm, CustomerForm
from .models import UserProfile, Stock, BuyStock, SellStock, Customer, Company, Invoice
from django.contrib.auth import authenticate, login, logout
from django.db.models import Sum
# from django.contrib.auth.models import User
from django.contrib import messages
from django.conf import settings

# template email sent
from django.core.mail import send_mail, EmailMultiAlternatives
from django.utils.html import strip_tags
from django.template.loader import render_to_string

# reset email
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.core.mail import EmailMultiAlternatives
from django.core.mail import send_mail, BadHeaderError
from django import template

# -------end--------

# password set
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
                return redirect('login')
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


@login_required(login_url='login')
def adminpage(request):
    form = InternalUserForm()
    loggedin_user = UserProfile.objects.get(user=request.user)
    mycompany = UserProfile.objects.get(user=request.user).company
    myuser = UserProfile.objects.filter(
        company=mycompany
    )
    userProfile = UserProfile.objects.get(user=request.user)
    company_name = userProfile.company
    superuser = company_name.super_user

    all_inventory = Stock.objects.filter(user=superuser)
    remaining = []

    try:
        for my in all_inventory:

            buy_sum_query = BuyStock.objects.filter(buy_inventory=my).aggregate(
                Sum('quantity'))['quantity__sum']

            sell_sum_query = SellStock.objects.filter(sell_inventory=my).aggregate(
                Sum('quantity'))['quantity__sum']

            # buy_values = buy_sum_query.values()
            # sell_values = sell_sum_query.values()

            print("buy:", buy_sum_query)
            print("sell:", sell_sum_query)

            tot = [my, buy_sum_query-sell_sum_query,
                   my.current_price, my.event_date]

            remaining.append(tot)

    except Exception:
        print(Exception)
        pass
    print("sum query: ", remaining)

    total = myuser.count()
    total_inventory = all_inventory.count()

    print(request.user.company.company_name)

    context = {"form": form, "total": total,
               "all": all_inventory, "total_inventory": total_inventory,
               "loggedin_user": loggedin_user, "final": remaining}
    return render(request, 'admin.html', context)


@login_required(login_url='login')
def userpage(request):
    loggedin_user = UserProfile.objects.get(user=request.user)
    sell = SellStock.objects.filter(user=request.user)
    buy = BuyStock.objects.filter(user=request.user)
    total_sell = sell.count()
    total_buy = buy.count()
    context = {"total_sell": total_sell,
               "total_buy": total_buy, "loggedin_user": loggedin_user}
    return render(request, 'user.html', context)


@login_required(login_url='login')
def add_new_user(request):
    user = request.user
    userProfile = UserProfile.objects.get(user=user)
    company_name = userProfile.company
    form = InternalUserForm()
    if request.method == 'POST':
        form = InternalUserForm(request.POST)
        if form.is_valid():
            email = request.POST.get('email')
            try:
                user_exist = User.objects.get(username=email)
            except Exception:
                user_exist = None
            if user_exist is None:
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

                first_name = newuser.first_name
                company = company_name
                username = newuser.username
                passcode = passcode

                msg_html = render_to_string('email_temp.html',
                                            {'first_name': first_name, 'company': company, 'username': username, 'password': passcode})
                text_content = strip_tags(msg_html)

                email = EmailMultiAlternatives(
                    # title
                    f'Mail From {company_name} company admin',

                    # context
                    text_content,

                    # from email
                    settings.EMAIL_HOST_USER,

                    # to email
                    [newuser.email],
                )
                email.attach_alternative(msg_html, "text/html")
                email.send()
            else:
                messages.info(request, "User Already Exist")

            # email_from = settings.EMAIL_HOST_USER
            # recipient_list = [newuser.email, ]
            # send_mail(subject, message, email_from, recipient_list)
            return redirect('admin_page')

    context = {"form": form}
    return render(request, 'admin.html', context)


@login_required(login_url='login')
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


@login_required(login_url='login')
def myusers(request):
    mycompany = UserProfile.objects.get(user=request.user).company
    myuser = UserProfile.objects.filter(
        company=mycompany
    )
    total = myuser.count()
    context = {"myuser": myuser, "total": total}
    return render(request, 'myuser.html', context)


@login_required(login_url='login')
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


@login_required(login_url='login')
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

            # stock_inventory = Stock.objects.get(id=get_inventory)
            # print("stock: ", stock_inventory)
            # final = stock_inventory.quantity + int(get_quantity)
            # print("final: ", final)
            # stock_inventory.quantity = final
            # stock_inventory.save()
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


@login_required(login_url='login')
def sell_inventory(request):
    # form = SellStockForm()
    userProfile = UserProfile.objects.get(user=request.user)
    company_name = userProfile.company
    superuser = company_name.super_user
    inventory = Stock.objects.filter(user=superuser)
    # form.fields['sell_inventory'].queryset = Stock.objects.filter(
    #     user=superuser)
    # if request.method == 'POST':
    #     # form = SellStockForm(request.POST)
    #     get_inventory = request.POST.get('sell_inventory')
    #     print("product", get_inventory)
    #     get_quantity = request.POST.get('quantity')
    #     selling_price = request.POST.get('selling_price')
    #     # total_price = unit_price.current_price*get_quantity
    #     sell = SellStock.objects.create(
    #         user=request.user,
    #         sell_inventory=get_inventory,
    #         quantity=get_quantity,
    #         selling_price=selling_price,

    #     )

    #     # sell.save()
    #     inventory_split = get_inventory.split("-")
    #     inventory_id = inventory_split[1]
    #     stock_inventory = Stock.objects.get(id=inventory_id)
    #     print("stock: ", stock_inventory)
    #     final = stock_inventory.quantity - int(get_quantity)
    #     print("final: ", final)
    #     stock_inventory.quantity = final
    #     stock_inventory.save()
    #     return redirect('sell_stock')
    mycompany = UserProfile.objects.get(user=request.user).company
    myuser = UserProfile.objects.filter(
        company=mycompany
    )

    all_sell = []
    for my in myuser:
        sell = SellStock.objects.filter(user=my.user)
        all_sell.append(sell)

    json_data = serializers.serialize('json', inventory)

    # print("data: ", json_data)

    context = {"all_sell": all_sell,
               "inventory": inventory, "json_data": json_data}
    return render(request, 'sell_stock.html', context)


@login_required(login_url='login')
def invoice_data(request):
    userProfile = UserProfile.objects.get(user=request.user)
    company_name = userProfile.company
    superuser = company_name.super_user
    inventory = Stock.objects.filter(user=superuser)
    form = CustomerForm()
    customer_data = Customer.objects.filter(
        user=company_name
    )
    company = Company.objects.get(super_user=superuser)
    last_invoice_no = company.last_invoice
    new_invoice_no = last_invoice_no + 1
    print("invoice", new_invoice_no)

    if request.method == 'POST':
        # print("xyz: ", request.body)

        data = json.loads(request.body)
        print("data2: ", data['data_obj'][0])
        print("data1: ", data['invoice_obj'][0])

        for bill in data['invoice_obj']:
            invoice = Invoice.objects.create(
                user=company_name,
                staff=request.user,
                invoice_number=bill['invoice_no'],
                customer_id=bill['customer'],
                invoice_date=bill['invoice_date'],
                due_date=bill['due_date'],
                discount=bill['discount'],
                total_bill=bill['total'],
            )

        for sell_data in data['data_obj']:
            inventry_item = sell_data['sell_inventory']

            SellStock.objects.create(
                user=request.user,
                sell_inventory=inventry_item,
                quantity=sell_data['quantity'],
                selling_price=sell_data['selling_price'],
                invoiceid=invoice.id,
            )
            # stock_inventory = Stock.objects.get(id=inventory_id)
            # print("stock: ", stock_inventory)
            # final = stock_inventory.quantity - int(get_quantity)
            # print("final: ", final)
            # stock_inventory.quantity = final
            # stock_inventory.save()
            company.last_invoice = new_invoice_no
            company.save()
            print("success")
        return redirect('sell_stock')
        # return JsonResponse({"msg": "Hello"})
    print("failed")

    json_data = serializers.serialize('json', inventory)
    customer_json = serializers.serialize('json', customer_data)

    # inventory_split = get_inventory.split("-")
    # inventory_id = inventory_split[1]
    # stock_inventory = Stock.objects.get(id=inventory_id)
    # print("stock: ", stock_inventory)
    # final = stock_inventory.quantity - int(get_quantity)
    # print("final: ", final)
    # stock_inventory.quantity = final
    # stock_inventory.save()
    # return redirect('sell_stock')

    context = {"inventory": inventory, "json_data": json_data,
               "form": form, "customer": customer_data, "customer_json": customer_json, "company_name": company_name, "new_invoice_no": new_invoice_no}
    return render(request, 'invoice.html', context)


@login_required(login_url='login')
def all_invoice(request):
    userProfile = UserProfile.objects.get(user=request.user)
    company_name = userProfile.company
    all_invoice = Invoice.objects.filter(user=company_name)
    total_invoice = all_invoice.count()
    context = {"invoice": all_invoice, "total": total_invoice}
    return render(request, 'sell_invoice.html', context)


@login_required(login_url='login')
def view_invoice(request, pk):
    userProfile = UserProfile.objects.get(user=request.user)
    company_name = userProfile.company
    invoice = Invoice.objects.get(id=pk)
    person = Customer.objects.get(id=invoice.customer_id)
    inventory = SellStock.objects.filter(invoiceid=pk)
    sumTotal = 0
    for inv in inventory:
        total = inv.quantity * inv.selling_price
        sumTotal += total
    print("sum: ", sumTotal)

    context = {"invoice": invoice,
               "company_name": company_name, "person": person, "inventory": inventory, "sumTotal": sumTotal}
    return render(request, 'view_invoice.html', context)


@login_required(login_url='login')
def edit_invoice(request, pk):
    form = CustomerForm()
    userProfile = UserProfile.objects.get(user=request.user)
    company_name = userProfile.company
    invoice = Invoice.objects.get(id=pk)
    person = Customer.objects.get(id=invoice.customer_id)
    customer_data = Customer.objects.filter(
        user=company_name
    )
    filtered_inventory = SellStock.objects.filter(invoiceid=pk)
    superuser = company_name.super_user
    inventory = Stock.objects.filter(user=superuser)
    json_data = serializers.serialize('json', inventory)
    customer_json = serializers.serialize('json', customer_data)
    filtered_inventory_json = serializers.serialize('json', filtered_inventory)

    context = {"invoice": invoice,
               "company_name": company_name, "person": person, "form": form, "customer": customer_data,
               "filtered_inventory": filtered_inventory, "inventory": inventory,
               "customer_json": customer_json, "json_data": json_data, "filtered_inventory_json": filtered_inventory_json}

    return render(request, 'edit_invoice.html', context)


@login_required(login_url='login')
def editInvoicedone(request, pk):
    if request.method == 'POST':

        data = json.loads(request.body)

        invoice_data = data['invoice_obj'][0]
        stock_data = data['data_obj']
        print('invoice', invoice_data)
        print('stock: ', stock_data)
        print(invoice_data['invoice_no'])
        invoice = Invoice.objects.get(id=pk)
        print("invoice get", invoice)
        print("customer: ", invoice_data['customer'])

        invoice.invoice_number = invoice_data['invoice_no']
        invoice.customer_id = int(invoice_data['customer'])
        invoice.invoice_date = invoice_data['invoice_date']
        invoice.due_date = invoice_data['due_date']
        invoice.discount = invoice_data['discount']
        invoice.total_bill = invoice_data['total']
        invoice.save()
        print("success")

        stock = SellStock.objects.filter(invoiceid=pk)
        for s in stock:
            s.delete()

        for sell in stock_data:
            SellStock.objects.create(
                user=request.user,
                sell_inventory=sell['sell_inventory'],
                quantity=sell['quantity'],
                selling_price=sell['selling_price'],
                invoiceid=pk,
            )

        return redirect('sell_invoice')

        print("stock filter", stock)

    context = {}
    return render(request, 'edit_invoice.html', context)


@login_required(login_url='login')
def add_customer(request):
    form = CustomerForm()
    userProfile = UserProfile.objects.get(user=request.user)
    company_name = userProfile.company

    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            customer = form.save(commit=False)
            customer.user = company_name
            customer.save()
            return redirect('invoice_data')
    context = {"form": form}
    return render(request, 'invoice.html', context)


@login_required(login_url='login')
def password_reset_request(request):
    if request.method == "POST":
        data = request.POST.get('email')
        # if password_reset_form.is_valid():
        # data = password_reset_form.cleaned_data['email']
        associated_users = User.objects.filter(
            Q(email=data) | Q(username=data))
        if associated_users.exists():
            for user in associated_users:
                subject = "Password Reset Requested"
                plaintext = template.loader.get_template(
                    'password_reset_email.txt')
                htmltemp = template.loader.get_template(
                    'password_reset_email.html')
                c = {
                    "email": user.email,
                    'domain': '127.0.0.1:8000',
                    'site_name': 'Website',
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "user": user,
                    'token': default_token_generator.make_token(user),
                    'protocol': 'http',
                }
                text_content = plaintext.render(c)
                html_content = htmltemp.render(c)
                try:
                    msg = EmailMultiAlternatives(subject, text_content, 'Website <influence1405@gmail.com>', [
                        user.email], headers={'Reply-To': 'mudassirzeya206@gmail.com'})
                    msg.attach_alternative(html_content, "text/html")
                    msg.send()
                except BadHeaderError:
                    return HttpResponse('Invalid header found.')
                messages.info(
                    request, "Password reset instructions have been sent to the email address entered.")
                return redirect("password_reset_done")
    # password_reset_form = PasswordResetForm()
    return render(request=request, template_name="login.html", context={"password_reset_form": "Invalid Username"})
