from django.contrib import admin
from .models import Product, Category, SkinType, Reviews


admin.site.register(Product)
admin.site.register(Category)
admin.site.register(SkinType)
admin.site.register(Reviews)
