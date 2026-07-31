from django.shortcuts import render

def account_home(request):
    return render(request, 'accounts/account_home.html')
def login_view(request):
    return render(request, 'accounts/login.html')
def signup_view(request):
    return render(request, 'accounts/signup.html')

from .models import Customer
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model

User = get_user_model()
from django.contrib.auth import authenticate, login, get_user_model

User = get_user_model()

def signup_view(request):
    if request.method == 'POST':
        if User.objects.filter(email=request.POST['email']).exists():
            return render(request, 'accounts/signup.html', {
            'error': 'Email already exists!'
            })
        Customer.objects.create(
            name=request.POST['name'],
            email=request.POST['email'],
            phone=request.POST['phone'],
            password=request.POST['password']
        )

        User.objects.create_user(
    username=request.POST['email'],
    email=request.POST['email'],
    password=request.POST['password']
)
        return redirect('account_login')

    return render(request, 'accounts/signup.html')



def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        try:
            customer = Customer.objects.get(
                email=email,
                password=password
            )


            user = authenticate(
               request,
               username=email,
               password=password
            )

            if user is not None:
               login(request, user)

            request.session['customer_id'] = customer.id
            request.session['customer_name'] = customer.name

            return redirect('account_home')

        except Customer.DoesNotExist:
            return render(request, 'accounts/login.html', {
                'error': 'Invalid Email or Password'
            })

    return render(request, 'accounts/login.html')

def logout_view(request):
    request.session.flush()
    return redirect('account_home')


def edit_profile(request):

    if 'customer_id' not in request.session:
        return redirect('account_login')

    customer = Customer.objects.get(
        id=request.session['customer_id']
    )

    if request.method == "POST":

       customer.name = request.POST["name"]
       customer.email = request.POST["email"]
       customer.phone = request.POST["phone"]

       customer.save()

       return redirect("account_home")

    return render(
        request,
        'accounts/edit_profile.html',
        {
            'customer': customer
        }
    )



def saved_address(request):

    if 'customer_id' not in request.session:
        return redirect('account_login')

    customer = Customer.objects.get(
        id=request.session['customer_id']
    )

    if request.method == "POST":

        customer.address = request.POST["address"]
        customer.save()

        return redirect("account_home")

    return render(
        request,
        "accounts/saved_address.html",
        {
            "customer": customer
        }
    )



def change_password(request):

    if 'customer_id' not in request.session:
        return redirect('account_login')

    customer = Customer.objects.get(
        id=request.session['customer_id']
    )

    if request.method == "POST":

        old_password = request.POST["old_password"]
        new_password = request.POST["new_password"]
        confirm_password = request.POST["confirm_password"]

        if customer.password != old_password:
            return render(
                request,
                "accounts/change_password.html",
                {
                    "error": "Old password is incorrect!"
                }
            )

        if new_password != confirm_password:
            return render(
                request,
                "accounts/change_password.html",
                {
                    "error": "Passwords do not match!"
                }
            )

        customer.password = new_password
        customer.save()


        user = User.objects.get(email=customer.email)

        user.set_password(new_password)

        user.save()

        request.session.flush()
        return redirect("account_login")

    return render(request, "accounts/change_password.html")