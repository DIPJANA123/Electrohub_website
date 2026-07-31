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
]


