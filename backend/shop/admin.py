from django.contrib import admin
from .models import Category, Product, ProductImage, Cart, Order


admin.site.register(Category)


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 3


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'name',
        'seller',
        'category',
        'price',
        'is_approved',
    )

    list_filter = (
        'category',
        'is_approved',
    )

    search_fields = (
        'name',
        'seller__shop_name',
    )

    inlines = [ProductImageInline]


admin.site.register(Cart)
admin.site.register(Order)