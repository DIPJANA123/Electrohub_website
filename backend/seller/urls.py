from django.urls import path
from . import views


urlpatterns = [
    path('', views.seller_home, name='seller_home'),
    path('signup/', views.seller_signup, name='seller_signup'),
    path('login/', views.seller_login, name='seller_login'),
    path('dashboard/', views.seller_dashboard, name='seller_dashboard'),
    path('add-product/', views.add_product, name='add_product'),
    path('my-products/', views.my_products, name='my_products'),
    path('orders/', views.seller_orders, name='seller_orders'),
]