from django.urls import path
from . import views

urlpatterns = [
    path('', views.account_home, name='account_home'),
    path('login/', views.login_view, name='account_login'),
    path('signup/', views.signup_view, name='account_signup'),
    path('logout/', views.logout_view, name='account_logout'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('saved-address/', views.saved_address, name='saved_address'),
    path('change-password/', views.change_password, name='change_password'),
]