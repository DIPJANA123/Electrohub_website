# from django.urls import path
# from . import views

# urlpatterns = [
#     path('signup/', views.signup_view, name='signup'),
#     path('login/', views.login_view, name='login'),
#     path('logout/', views.logout_view, name='logout'),
# ]


# from django.urls import path
# from . import views

# urlpatterns = [
#     path('', views.product_list, name='shop'),
#     path('product/<int:pk>/', views.product_detail, name='product_detail'),
#     path('cart/', views.cart_view, name='cart'),
#     path('checkout/', views.checkout, name='checkout'),
#     path('orders/', views.orders, name='orders'),
# ]

from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]

