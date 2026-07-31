from django.db import models
from django.conf import settings
from seller.models import Seller


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Product(models.Model):

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    seller = models.ForeignKey(
        Seller,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    name = models.CharField(max_length=200)

    price = models.IntegerField()

    description = models.TextField(blank=True)

    image = models.ImageField(
        upload_to='products/',
        blank=True,
        null=True
    )

    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return self.name


# Multiple Images for Product
class ProductImage(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='images'
    )

    image = models.ImageField(upload_to='products/')

    def __str__(self):
        return f"{self.product.name} Image"


class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.user} - {self.product}"


class Order(models.Model):
    PAYMENT_CHOICES = (
        ('COD', 'Cash On Delivery'),
        ('UPI', 'UPI'),
    )

    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    product = models.ForeignKey(
    Product,
    on_delete=models.CASCADE,
    null=True,
    blank=True
)
    total = models.IntegerField(default=0)
    address = models.TextField()
    phone = models.CharField(max_length=15)
    payment_method = models.CharField(max_length=10, choices=PAYMENT_CHOICES)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Pending'
    )

    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id}"