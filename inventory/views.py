from django.shortcuts import render

def view_bag(request):
    """A view that renders the inventory admin page"""
    return render(request, 'inventory/inventory_admin.html')
