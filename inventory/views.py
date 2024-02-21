from django.shortcuts import render

from products.views import get_products_and_sorting

def view_bag(request):
    """A view that renders the inventory admin page"""
    return get_products_and_sorting(request, 'inventory/inventory_admin.html')
