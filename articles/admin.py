from django.contrib import admin
from .models import Article


class ArticleAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'created_on',
        'status',
    )

    ordering = (
        'title',
        'created_on',
        'status',
        )

admin.site.register(Article, ArticleAdmin)
