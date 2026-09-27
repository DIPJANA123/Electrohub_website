from django.contrib import admin
from .models import Category, Product, ProductImage, Cart, Order,Wishlist,ProductReview, ReplacementRequest


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




@admin.register(ReplacementRequest)
class ReplacementRequestAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'order',
        'product',
        'reason',
        'status',
        'created'
    )

    list_filter = (
        'status',
        'reason',
        'created'
    )

    search_fields = (
        'user__username',
        'product__name',
        'order__id'
    )

    list_editable = (
        'status',
    )

    readonly_fields = (
        'created',
        'updated',
    )    


admin.site.register(Cart)
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'user',
        'product',
        'total',
        'status',
        'created',
        'expected_delivery_date',
    )

    list_filter = (
        'status',
        'payment_method',
        'created',
    )

    search_fields = (
        'user__username',
        'product__name',
        'phone',
    )

    readonly_fields = (
        'created',
        'confirmed_at',
        'shipped_at',
        'out_for_delivery_at',
        'delivered_at',
    )

    fieldsets = (
        ('Order Information', {
            'fields': (
                'user',
                'product',
                'total',
                'address',
                'phone',
                'payment_method',
                'status',
            )
        }),

        ('Delivery Timeline', {
            'fields': (
                'created',
                'confirmed_at',
                'shipped_at',
                'out_for_delivery_at',
                'delivered_at',
                'expected_delivery_date',
            )
        }),
    )


def save_model(self, request, obj, form, change):
    from django.utils import timezone

    if change:
        old_obj = Order.objects.get(pk=obj.pk)

        if old_obj.status != obj.status:

            if obj.status == 'Confirmed':
                obj.confirmed_at = timezone.now()

            elif obj.status == 'Shipped':
                obj.shipped_at = timezone.now()

            elif obj.status == 'Out for Delivery':
                obj.out_for_delivery_at = timezone.now()

            elif obj.status == 'Delivered':
                obj.delivered_at = timezone.now()

    super().save_model(request, obj, form, change)    
admin.site.register(Wishlist)
admin.site.register(ProductReview)