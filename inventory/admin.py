from django.contrib import admin
from .models import InventoryItem


class InventoryItemAdmin(admin.ModelAdmin):
    list_display = (
        'product',
        'min_threshold',
        'min_order_quantity',
        'supplier_name',
        'supplier_email',
        'last_reorder_date',
        'is_expecting_delivery',
        'ordered_quantity',
        'cost_per_product',
        'total_units_sold',
        'total_lost_or_damaged',
        'total_revenue_generated',
    )

    ordering = (
        'product',
        'min_threshold',
        'min_order_quantity',
        'supplier_name',
        'supplier_email',
        'last_reorder_date',
        'is_expecting_delivery',
        'ordered_quantity',
        'cost_per_product',
        'total_units_sold',
        'total_lost_or_damaged',
        'total_revenue_generated',
    )


admin.site.register(InventoryItem, InventoryItemAdmin)
