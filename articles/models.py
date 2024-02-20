from django.db import models

from products.models import Category, Product, SkinType

STATUS = ((0, "Archived"), (1, "Published"))


class Article(models.Model):
    title = models.CharField(max_length=200, unique=True)
    content = models.TextField(blank=False)
    image = models.ImageField(null=True, blank=True)
    created_on = models.DateTimeField(auto_now=True)
    status = models.IntegerField(choices=STATUS, default=1)
    category = models.ForeignKey(
        'products.Category', null=True, blank=True, on_delete=models.SET_NULL
    )
    product = models.ForeignKey(
        'products.Product', null=True, blank=True, on_delete=models.SET_NULL
    )
    skin_type = models.ForeignKey(
        'products.SkinType', null=True, blank=True, on_delete=models.SET_NULL
    )

    ordering = ['-created_on']

    def __str__(self):
        return self.title
