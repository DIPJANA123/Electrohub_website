from django.shortcuts import render, redirect
from .models import Seller
from shop.models import Category
from shop.models import Product, Category
from seller.models import Seller
from shop.models import Product
from shop.models import Order

def seller_home(request):
    return render(request, 'seller/seller_home.html')

def seller_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        try:
            seller = Seller.objects.get(email=email, password=password)

            request.session['seller_id'] = seller.id
            request.session['seller_name'] = seller.shop_name

            return redirect('seller_dashboard')

        except Seller.DoesNotExist:
            return render(request, 'seller/login.html', {
                'error': 'Invalid Email or Password'
            })

    return render(request, 'seller/login.html')

def seller_signup(request):
    if request.method == 'POST':
        shop_name = request.POST['shop_name']
        owner_name = request.POST['owner_name']
        email = request.POST['email']
        phone = request.POST['phone']
        password = request.POST['password']

        if Seller.objects.filter(email=email).exists():
            return render(request, 'seller/signup.html', {
                'error': 'Email already exists!'
            })

        Seller.objects.create(
            shop_name=shop_name,
            owner_name=owner_name,
            email=email,
            phone=phone,
            password=password
        )

        return redirect('seller_login')

    return render(request, 'seller/signup.html')


def seller_dashboard(request):

    if 'seller_id' not in request.session:
        return redirect('seller_login')

    seller_name = request.session['seller_name']

    return render(request, 'seller/dashboard.html', {
        'seller_name': seller_name
    })

def add_product(request):
    return render(request, 'seller/add_product.html')


def add_product(request):

    categories = Category.objects.all()

    return render(
        request,
        'seller/add_product.html',
        {
            'categories': categories
        }
    )



def add_product(request):

    if 'seller_id' not in request.session:
        return redirect('seller_login')

    categories = Category.objects.all()

    if request.method == 'POST':

        seller = Seller.objects.get(id=request.session['seller_id'])

        Product.objects.create(
            seller=seller,
            name=request.POST['name'],
            category=Category.objects.get(id=request.POST['category']),
            price=request.POST['price'],
            description=request.POST['description'],
            image=request.FILES['image'],
            is_approved=False
        )

        return redirect('seller_dashboard')

    return render(
        request,
        'seller/add_product.html',
        {'categories': categories}
    )




def my_products(request):
    if 'seller_id' not in request.session:
        return redirect('seller_login')

    seller_id = request.session['seller_id']

    products = Product.objects.filter(seller_id=seller_id)

    return render(
        request,
        'seller/my_product.html',
        {'products': products}
    )




def seller_orders(request):

    if 'seller_id' not in request.session:
        return redirect('seller_login')

    seller = Seller.objects.get(id=request.session['seller_id'])

    if request.method == "POST":

        order = Order.objects.get(id=request.POST["order_id"])

        order.status = request.POST["status"]

        order.save()

    orders = Order.objects.filter(product__seller=seller)

    return render(
        request,
        'seller/seller_orders.html',
        {
            'orders': orders
        }
    )