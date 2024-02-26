from django.contrib import admin
from .models import Product, Category, SkinType, Reviews


class ProductAdmin(admin.ModelAdmin):
    """
    Admin options for the Product model.
    """
    list_display = (
        'sku',
        'name',
        'category',
        'skin_type',
        'quantity',
        'price',
        'rating',
        'image',
    )

    ordering = ('sku', 'category', 'skin_type', 'rating')


class CategoryAdmin(admin.ModelAdmin):
    """
    Admin options for the Category model.
    """
    list_display = (
        'friendly_name',
        'name',
    )


class SkinTypeAdmin(admin.ModelAdmin):
    """
    Admin options for the SkinType model.
    """
    list_display = (
        'friendly_name',
        'name',
    )


class ReviewsAdmin(admin.ModelAdmin):
    """
    Admin options for the Reviews model.
    """
    list_display = (
        'product',
        'user',
        'comment',
        'rating',
    )


admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(SkinType, SkinTypeAdmin)
admin.site.register(Reviews, ReviewsAdmin)
