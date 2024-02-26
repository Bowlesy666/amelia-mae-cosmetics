from django.contrib import admin
from .models import Article


class ArticleAdmin(admin.ModelAdmin):
    """
    Admin view configuration for the Article model.
    """
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
