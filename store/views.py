from django.shortcuts import render
from .models import * 
from django.http import JsonResponse
import datetime
import json
from . utils import cookieCart
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.shortcuts import redirect
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .models import Customer

def store(request):

     if request.user.is_authenticated:
          customer = request.user.customer
          order, created = Order.objects.get_or_create(customer=customer, complete=False)
          items = order.orderitem_set.all()
          cartItems = order.get_cart_items
     else:
            cookieData = cookieCart(request)
            cartItems = cookieData['cartItems']

     products = Product.objects.all()
     context = {'products':products, 'cartItems': cartItems}
     return render(request, 'store/store.html', context)


from django.shortcuts import render

def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        cookieData = cookieCart(request)
        cartItems = cookieData['cartItems']
        order = cookieData['order']
        items = cookieData['items']

    # Ensure this context and return statement are outside the `else` block
    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/cart.html', context)



def checkout(request):
     if request.user.is_authenticated:
          customer = request.user.customer
          order, created = Order.objects.get_or_create(customer=customer, complete=False)
          items = order.orderitem_set.all()
          cartItems = order.get_cart_items
     else:
          cookieData = cookieCart(request)
          cartItems = cookieData['cartItems']
          order = cookieData['order']
          items = cookieData['items']
     
     context = {'items':items, 'order':order, 'cartItems': cartItems}
     return render(request, 'store/checkout.html', context)
def updateItem(request):
     data = json.loads(request.body)
     productId = data['productId']
     action = data['action']
     print('Action:', action)
     print('Product:', productId)

     customer = request.user.customer
     product = Product.objects.get(id=productId)
     order, created = Order.objects.get_or_create(customer=customer, complete=False)

     orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

     if action == 'add':
          orderItem.quantity = (orderItem.quantity + 1)
     elif action == 'remove':
          orderItem.quantity = (orderItem.quantity - 1)

     orderItem.save()

     if orderItem.quantity <= 0:
          orderItem.delete()

     return JsonResponse('Item was added', safe=False)
from django.views.decorators.csrf import csrf_exempt
    
@csrf_exempt
def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        # For authenticated users, retrieve the order from the database
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        total = float(data['form']['total'])  # Total is sent from the frontend
        order.transaction_id = transaction_id
    else:
        # For non-authenticated users, retrieve order data from cookies
        cookieData = cookieCart(request)
        order = cookieData['order']
        total = cookieData['order']['get_cart_total']  # Get total from cookie data

    # Now you can safely compare total
    if total == float(order['get_cart_total']):  # Make sure to compare float values
        # If the totals match, mark the order as complete
        if request.user.is_authenticated:
            order.complete = True
            order.save()

        # If shipping is enabled, create a shipping address
        if order.get('shipping', False):  # Access 'shipping' from dictionary if non-authenticated
            ShippingAddress.objects.create(
                customer=request.user.customer if request.user.is_authenticated else None,
                order=order,
                address=data['shipping']['address'],
                city=data['shipping']['city'],
                state=data['shipping']['state'],
                zipcode=data['shipping']['zipcode'],
            )
    
    return JsonResponse('Payment submitted..', safe=False)


def sign_up(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Create the user
            user.is_admin = True  # Set the user as a superuser
            user.is_staff = True  # Ensure the user has staff privileges
            user.is_superuser = True
            user.save()  # Save the updated user object

            auth_login(request, user)  # Log the user in immediately using the correct function

            # Create a Customer object and save it to the database
            customer = Customer.objects.create(
                user=user,  # Associate the user with the customer
                name=request.POST.get('name', ''),  # Get the name from form or set an empty string
                email=user.email  # Use the user's email
            )
            customer.save()

            messages.success(request, 'Account created successfully and you are now an admin!')
            return redirect('login')  # Redirect to the login page after successful signup
        else:
            messages.error(request, 'Error occurred during signup')
    else:
        form = UserCreationForm()

    return render(request, 'store/signup.html', {'form': form})

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('store')  # Redirect to the store page after login
        else:
            messages.error(request, "Invalid credentials")
    return render(request, 'store/login.html')

def logout(request):
    auth_logout(request)
    return redirect('login')