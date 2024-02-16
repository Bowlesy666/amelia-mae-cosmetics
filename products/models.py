from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class Category(models.Model):
    """ Model representing the product category """
    class Meta:
        verbose_name_plural = 'Categories'

    name = models.CharField(max_length=254)
    friendly_name = models.CharField(max_length=254, null=True, blank=True)

    def __str__(self):
        """ String to represent the Category object """
        return self.name

    def get_friendly_name(self):
        """ Method to return the friendly name of the Category """
        return self.friendly_name


class SkinType(models.Model):
    """ Model representing the skin types associated with products """
    name = models.CharField(max_length=254)
    friendly_name = models.CharField(max_length=254, null=True, blank=True)

    def __str__(self):
        """ String to represent the SkinType object """
        return self.name

    def get_friendly_name(self):
        """ Method to return the friendly name of the skin type """
        return self.friendly_name


class Reviews(models.Model):
    """ Model representing the product reviews """
    class Meta:
        verbose_name_plural = 'Reviews'
        ordering = ['-created_on']

    product = models.ForeignKey(
        'Product', on_delete=models.CASCADE, related_name='reviews',
        default=0)
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True)
    comment = models.CharField(max_length=254, null=True, blank=True)
    rating = models.DecimalField(
        max_digits=2, decimal_places=0,
        validators=[MinValueValidator(0),
        MaxValueValidator(5)]
    )
    created_on = models.DateTimeField(auto_now=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        """ String to represent the Reviews Object """
        return f"Review by {self.user.username}: {self.comment[:50]}..."


class Product(models.Model):
    """ Model representing a Product """
    category = models.ForeignKey(
        'Category', null=True, blank=True, on_delete=models.SET_NULL
    )
    skin_type = models.ForeignKey(
        'SkinType', on_delete=models.SET_NULL,
        max_length=100, null=True, blank=True)
    sku = models.CharField(max_length=254, null=True, blank=True)
    name = models.CharField(max_length=254)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    rating = models.DecimalField(
        max_digits=6, decimal_places=2, null=True, blank=True, default=0
    )
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    quantity = models.PositiveIntegerField(default=100)
    is_out_of_stock = models.BooleanField(default=False)
    is_discontinued = models.BooleanField(default=False)
    is_best_seller = models.BooleanField(default=False)

    def update_out_of_stock_status(self):
        """  Update the out of stock status based on the quantity. """
        if self.quantity == 0:
            self.is_out_of_stock = True
        else:
            self.is_out_of_stock = False

    def save(self, *args, **kwargs):
        """
        Override save method to update the out of stock status before saving.
        """
        self.update_out_of_stock_status()
        super().save(*args, **kwargs)

    def __str__(self):
        """ String to represent the Product object """
        return self.name
