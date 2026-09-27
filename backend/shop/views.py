from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import (
    Product,
    Cart,
    Order,
    Category,
    Wishlist,
    ProductReview,
    ReplacementRequest
)
from accounts.models import Customer


from django.http import HttpResponse, JsonResponse
from django.db.models import Avg
from rapidfuzz import process, fuzz



def smart_search(products, search):

    search = search.strip().lower()

    if not search:
        return products

    # 1. Normal partial search
    normal_results = products.filter(
        name__icontains=search
    )

    if normal_results.exists():
        return normal_results

    # 2. Typo-tolerant search
    all_products = list(products)

    product_names = [
        product.name
        for product in all_products
        if product.name
    ]

    if not product_names:
        return products.none()

    matches = process.extract(
        search,
        product_names,
        scorer=fuzz.WRatio,
        limit=20,
        score_cutoff=55
    )

    matched_names = [match[0] for match in matches]

    matched_products = [
        product
        for product in all_products
        if product.name in matched_names
    ]

    # Same order as RapidFuzz ranking
    matched_products.sort(
        key=lambda product: matched_names.index(product.name)
    )

    return matched_products



def search_suggestions(request):

    query = request.GET.get('q', '').strip()

    if not query:
        return JsonResponse([], safe=False)

    products = Product.objects.filter(
        is_approved=True,
        name__icontains=query
    )[:8]

    suggestions = []

    for product in products:
        suggestions.append({
            'id': product.id,
            'name': product.name,
            'price': product.price,
        })

    return JsonResponse(
        suggestions,
        safe=False
    )


# =========================================
# Homepage
# =========================================

def homepage(request):

    products = Product.objects.filter(is_approved=True)

    search = request.GET.get('search')
    category = request.GET.get('category')

    
    if search:
       products = smart_search(
        products,
        search
    )

    if category:
        products = products.filter(
            category__name=category
        )

    return render(
        request,
        'shop/homepage.html',
        {
            'products': products
        }
    )


# =========================================
# Product List
# =========================================

def product_list(request):

    products = Product.objects.all()

    return render(
        request,
        'shop/product_list.html',
        {
            'products': products
        }
    )


# =========================================
# Product Detail
# =========================================

def product_detail(request, id):

    product = get_object_or_404(
        Product,
        id=id
    )

    similar_products = Product.objects.filter(
        category=product.category,
        is_approved=True
    ).exclude(
        id=product.id
    ).annotate(
        average_rating=Avg('reviews__rating')
    )[:8]

    return render(
        request,
        'shop/product_detail.html',
        {
            'product': product,
            'similar_products': similar_products
        }
    )


# =========================================
# Add To Cart
# =========================================

@login_required
def add_to_cart(request, product_id):

    product = Product.objects.get(
        id=product_id
    )

    cart_item, created = Cart.objects.get_or_create(
        user=request.user,
        product=product
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('cart')


# =========================================
# Cart View
# =========================================

@login_required
def cart_view(request):

    items = Cart.objects.filter(
        user=request.user
    )

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


# =========================================
# Checkout
# =========================================

@login_required
def checkout(request):

    items = Cart.objects.filter(
        user=request.user
    )

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


# =========================================
# Orders
# =========================================

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


# =========================================
# Remove Cart
# =========================================

@login_required
def remove_cart(request, item_id):

    item = Cart.objects.get(
        id=item_id,
        user=request.user
    )

    item.delete()

    return redirect('cart')


# =========================================
# Increase Cart
# =========================================

@login_required
def increase_cart(request, item_id):

    item = Cart.objects.get(
        id=item_id,
        user=request.user
    )

    item.quantity += 1
    item.save()

    return redirect('cart')


# =========================================
# Decrease Cart
# =========================================

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


# =========================================
# Order Success
# =========================================

def order_success(request):

    return render(
        request,
        'shop/order_success.html'
    )


# =========================================
# Add To Wishlist
# =========================================

def add_to_wishlist(request, product_id):

    if not request.user.is_authenticated:
        return redirect('login')

    product = Product.objects.get(
        id=product_id
    )

    Wishlist.objects.get_or_create(
        user=request.user,
        product=product
    )

    return redirect(
        'product_detail',
        id=product.id
    )


# =========================================
# Add Review
# =========================================

def add_review(request, product_id):

    if not request.user.is_authenticated:
        return redirect('account_login')

    product = Product.objects.get(
        id=product_id
    )

    if request.method == "POST":

        rating = request.POST.get("rating")
        comment = request.POST.get("comment")

        ProductReview.objects.update_or_create(
            user=request.user,
            product=product,
            defaults={
                "rating": rating,
                "comment": comment
            }
        )

        return redirect(
            'product_detail',
            id=product.id
        )

    return redirect(
        'product_detail',
        id=product.id
    )


# =========================================
# Request Replacement
# =========================================

def request_replacement(request, order_id):

    if not request.user.is_authenticated:
        return redirect('account_login')

    order = get_object_or_404(
        Order,
        id=order_id,
        user=request.user
    )

    if order.status != "Delivered":
        return redirect('orders')

    if request.method == "POST":

        reason = request.POST.get('reason')
        description = request.POST.get('description')

        ReplacementRequest.objects.create(
            user=request.user,
            order=order,
            product=order.product,
            reason=reason,
            description=description
        )

        return redirect('orders')

    return render(
        request,
        'shop/replacement_request.html',
        {
            'order': order
        }
    )




def recently_viewed_products(request):
    product_ids = request.GET.get('ids', '')

    if not product_ids:
        return JsonResponse([], safe=False)

    ids = product_ids.split(',')

    products = Product.objects.filter(
        id__in=ids,
        is_approved=True
    )

    product_data = []

    for product in products:
        product_data.append({
            'id': product.id,
            'name': product.name,
            'price': product.price,
            'image': product.image.url if product.image else '',
        })

    return JsonResponse(product_data, safe=False)