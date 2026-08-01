from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Product, Cart, Order, Category
from accounts.models import Customer

from django.http import HttpResponse



# Homepage
def homepage(request):

    products = Product.objects.filter(is_approved=True)

    search = request.GET.get('search')
    category = request.GET.get('category')

    if search:
        products = products.filter(name__icontains=search)

    if category:
        products = products.filter(category__name=category)

    return render(request, 'shop/homepage.html', {
        'products': products
    })
# def homepage(request):
#     products = Product.objects.all()

#     return render(request, 'shop/homepage.html', {
#         'products': products
#     })


# Product List
def product_list(request):
    products = Product.objects.all()

    return render(request,
                  'shop/product_list.html',
                  {'products': products})


# Product Detail
def product_detail(request, id):
    product = get_object_or_404(Product, id=id)

    return render(request,
                  'shop/product_detail.html',
                  {'product': product})


# Add To Cart
@login_required
def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)

    cart_item, created = Cart.objects.get_or_create(
        user=request.user,
        product=product
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('cart')


# Cart View
@login_required
def cart_view(request):
    items = Cart.objects.filter(user=request.user)

    total = sum(
        item.product.price * item.quantity
        for item in items
    )

    return render(
        request,
        'shop/cart.html',
        {
        'items': items,
        'total': total
        }
    )

   


# Checkout
@login_required
def checkout(request):
    items = Cart.objects.filter(user=request.user)

    if request.method == "POST":

        total = sum(
            i.product.price * i.quantity
            for i in items
        )

        first_item = items.first()

        if first_item is None:
           return redirect('cart')

        order = Order.objects.create(
    user=request.user,
    product=first_item.product,
    total=total,
    address=request.POST['address'],
    phone=request.POST['phone'],
    payment_method=request.POST['payment_method']
)

        items.delete()

        return redirect('order_success')
    
    # customer = Customer.objects.get(
    #     email=request.user.email
    # )
    customer = Customer.objects.filter(
        email=request.user.email
    ).first()

    if customer is None:
        return HttpResponse(
        f"Customer not found.<br>"
        f"Logged in email: {request.user.email}"
    )

    return render(
    request,
    'shop/checkout.html',
    {
        'items': items,
        'customer': customer
    }
)

# Orders


@login_required
def orders(request):

    my_orders = Order.objects.filter(
        user=request.user
    )

    return render(
        request,
        'shop/orders.html',
        {
            'orders': my_orders
        }
    )



@login_required
def remove_cart(request, item_id):

    item = Cart.objects.get(
        id=item_id,
        user=request.user
    )

    item.delete()

    return redirect('cart')


@login_required
def increase_cart(request, item_id):

    item = Cart.objects.get(
        id=item_id,
        user=request.user
    )

    item.quantity += 1
    item.save()

    return redirect('cart')



@login_required
def decrease_cart(request, item_id):

    item = Cart.objects.get(
        id=item_id,
        user=request.user
    )

    if item.quantity > 1:
        item.quantity -= 1
        item.save()
    else:
        item.delete()

    return redirect('cart')



def order_success(request):
    return render(
        request,
        'shop/order_success.html'
    )