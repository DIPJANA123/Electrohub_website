from django.urls import path
from . import views

urlpatterns = [
    # Homepage
    path('', views.homepage, name='homepage'),

    # Product list
    path('products/', views.product_list, name='product_list'),

    # Product detail
    path('product/<int:id>/',
         views.product_detail,
         name='product_detail'),

    # Cart
    path('add-to-cart/<int:product_id>/',
         views.add_to_cart,
         name='add_to_cart'),

    path('cart/',
         views.cart_view,
         name='cart'),

     path('remove-cart/<int:item_id>/', 
          views.remove_cart,
          name='remove_cart'),  

     path('increase-cart/<int:item_id>/',
          views.increase_cart,
          name='increase_cart'),

     path('decrease-cart/<int:item_id>/',
          views.decrease_cart,
          name='decrease_cart'),       

    # Checkout
    path('checkout/',
         views.checkout,
         name='checkout'),

    # Orders
    path('orders/',
         views.orders,
         name='orders'),


    path('order-success/', views.order_success, name='order_success'), 


    path(
    'wishlist/add/<int:product_id>/',
    views.add_to_wishlist,
    name='add_to_wishlist'),   


    path(
    'product/<int:product_id>/review/',
    views.add_review,
    name='add_review'),


    path(
    'replacement/<int:order_id>/',
    views.request_replacement,
    name='request_replacement'),


    path(
    'search-suggestions/',
    views.search_suggestions,
    name='search_suggestions'),


    path(
    'recently-viewed/',
    views.recently_viewed_products,
    name='recently_viewed_products'),
]




