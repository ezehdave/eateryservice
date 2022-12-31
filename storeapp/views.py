from django.shortcuts import render
from . models import *
from django.http import JsonResponse
from django.shortcuts import render, redirect
import json
import datetime
from django.contrib.auth.forms import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .form import signUpForm, ProductForm
from django.db.models import Q
from django.contrib.auth.decorators import login_required
# Create your views here.

def loginpage(request):
    page = "login"
    if request.user.is_authenticated:
        return redirect('menu-list')

    if request.method == "POST":
        username = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "user does not exist")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("menu-list")
        else:
            messages.error(request, "password does not exist")

    context = {'page': page}
    return render(request, "storeapp/login.html", context)

def logoutUser(request):
    logout(request)
    return redirect('main')

def registerpage(request):
    form = signUpForm()
    if request.method == "POST":
       form = signUpForm(request.POST)
       if form.is_valid():
            user = form.save(commit=False)
            user.email= user.email.lower()
            user.save()
            login(request, user)
            return redirect("main")
       else:
           messages.error(request, "an error occured during registration")

    context = {'form':form}
    return render(request,'storeapp/login.html', context)


def main(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        cartItems = order.get_cart_items
    else:
        cartItems = 0
    context = {"cartItems":cartItems}
    return render(request, "storeapp/main.html", context)

def menuList(request):

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        cartItems = order['get_cart_items']

    q = request.GET.get('q') if request.GET.get('q') != None else ''
    products = Product.objects.filter(
        Q(product_type__name__icontains=q)
    )
    context = {"products": products, 'cartItems': cartItems}
    return render(request, "storeapp/menu-list.html",context)

def menuView(request, pk):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        cartItems = order['get_cart_items']


    menu = Product.objects.get(id=pk)
    context ={'menu': menu,'cartItems':cartItems}
    return render(request,"storeapp/menu.html",context)

def checkOut(request):
        if request.user.is_authenticated:
            customer = request.user.customer
            order, created = Order.objects.get_or_create(customer=customer, complete=False)
            items = order.orderitem_set.all()
            cartItems = order.get_cart_items

        else:
            items = []
            order = {'get_cart_total': 0, 'get_cart_items': 0}
            cartItems = order['get_cart_items']

        context = {"items": items, "order": order, 'cartItems':cartItems}
        return render(request, "storeapp/check-out.html", context)


@login_required(login_url='login')
def delivery(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items

    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}

    context = {"items": items, "order": order,"cartItems": cartItems}
    return render(request,"storeapp/delivery.html", context)

def about(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        cartItems = order.get_cart_items
    else:
        cartItems = 0
    context = {"cartItems": cartItems}
    return render(request, "storeapp/about.html", context)
def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
    cartItems = order.get_cart_items
    Customer_order = OrderItem.objects.filter(order__customer=customer, order__complete=False)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == "remove":
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()


    cartItems = order.get_cart_items
    data = []
    for obj in Customer_order:
        item = {
            'id': obj.product.id,
            'product':obj.product.name,
            'quantity':obj.quantity,
            'image': obj.product.image.url,
            'get_total': obj.get_total,
            'price': obj.product.price,



        }
        data.append(item)
    get_cart_total= obj.order.get_cart_total
    return JsonResponse({"data": data,"get_cart_total":get_cart_total,"cartItems":cartItems })


def ajaxUpdate(request):
    customer = request.user.customer
    Customer_order = OrderItem.objects.filter(order__customer=customer, order__complete=False )



    data = []
    for obj in Customer_order:
        item = {
            'id': obj.product.id,
            'product':obj.product.name,
            'quantity':obj.quantity,
            'image': obj.product.image.url,
            'get_total': obj.get_total,
            'price': obj.product.price,



        }
        data.append(item)
    get_cart_total= obj.order.get_cart_total
    return JsonResponse({"data": data,"get_cart_total":get_cart_total })


def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created =Order.objects.get_or_create(customer=customer, complete=False)
        total = float(data['form']['total'])

        order.transaction_id = transaction_id

        if total == order.get_cart_total:
            order.complete =True
        order.save()

        Delivery.objects.create(
            customer=customer,
            order=order,
            city=data['form']['city'],
            address=data['form']['street'],
            pickup_location=data['form']['pickup'],
            phone_number=data['form']['phone'],
            total=data['form']['total'],

        )

    else:
        print('User is not logged in...')
    return JsonResponse('payment is complete!', safe=False)


def orders(request):
    customer = request.user.customer
    ordered = Order.objects.filter(customer=customer)
    ordered_all= Order.objects.all()
    transaction_id = OrderItem.objects.filter(order__transaction_id=1662310505.914557)

    context = {"ordered": ordered, "transaction_id": transaction_id,"ordered_all":ordered_all}
    return render(request,"storeapp/deliverytext.html", context)


def cartNumber(request):

    customer = request.user.customer
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    cartItems = order.get_cart_items
    return JsonResponse({"data": cartItems})

def createProduct(request):
    form =ProductForm
    if request.method == "POST":
        form = ProductForm(request.POST,request.FILES,)
        if form.is_valid():
            form.save()
            return redirect("main")

    context = {"form": form}
    return render(request, "storeapp/product_form.html", context)

def historyPage(request):
    if Order.transaction_id  == None:
        orders = Order.transaction_id
        orders.delete()
    customer = request.user.customer
    ordered = Order.objects.filter(customer=customer)


    context = {"ordered": ordered}
    return render(request, "storeapp/history_page.html", context)

def TransactionPage(request, pk):
    customer = request.user.customer
    ordered = Order.objects.filter(customer=customer)
    ordereds = OrderItem.objects.filter(order__transaction_id=pk)
    transactionId = pk
    delivery =Delivery.objects.get(order__transaction_id=pk)
    context = {"ordereds":ordereds,"transactionId":transactionId,"delivery":delivery}

    return render(request, "storeapp/Transaction_page.html", context)









