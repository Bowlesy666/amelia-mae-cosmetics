from django.db import models

from products.models import Product


class InventoryItem(models.Model):
    """
    Represents an inventory item associated with a specific product.

    is_below_threshold method determines if the product quantity is
    below the minimum threshold.
    """
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    min_threshold = models.PositiveIntegerField(default=20)
    min_order_quantity = models.PositiveIntegerField(default=100)
    supplier_name = models.CharField(
        max_length=100, blank=False, default='Bowles Beauty Supplys')
    supplier_email = models.EmailField(
        max_length=254, blank=False, default='bowlesdevelopment906@gmail.com')
    last_reorder_date = models.DateField(null=True, blank=True)
    is_expecting_delivery = models.BooleanField(default=False)
    ordered_quantity = models.PositiveIntegerField(default=0)
    cost_per_product = models.DecimalField(
        max_digits=10, decimal_places=2, default=10
    )
    total_units_sold = models.PositiveIntegerField(default=0)
    total_lost_or_damaged = models.PositiveIntegerField(default=0)
    total_revenue_generated = models.DecimalField(
        max_digits=10, decimal_places=2, default=0
    )

    def __str__(self):
        return f"Inventory Item for {self.product.name}"

    def is_below_threshold(self):
        """
        Checks if the current quantity of the associated product
        is below the minimum threshold.
        True if the product quantity is below the minimum threshold,
        False otherwise.
        """
        return self.product.quantity < self.threshold
