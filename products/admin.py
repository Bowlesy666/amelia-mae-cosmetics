from django.contrib import admin
from .models import Product, Category, SkinType, Reviews


class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'sku',
        'name',
        'category',
        'skin_type',
        'price',
        'rating',
        'image',
    )

    ordering = ('sku', 'category', 'skin_type', 'rating')


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'friendly_name',
        'name',
    )


class SkinTypeAdmin(admin.ModelAdmin):
    list_display = (
        'friendly_name',
        'name',
    )


class ReviewsAdmin(admin.ModelAdmin):
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
