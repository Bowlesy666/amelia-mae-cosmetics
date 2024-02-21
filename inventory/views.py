from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages

from products.views import get_products_and_sorting
from .models import InventoryItem
from products.models import Product
from .forms import InventoryItemForm

import json

def view_inventory(request):
    """A view that renders the inventory admin page"""
    return get_products_and_sorting(request, 'inventory/inventory_admin.html')


def edit_inventory_item(request, inventory_item_id):
    """ Edit a inventory items details in the store """
    inventory_item = get_object_or_404(InventoryItem, pk=inventory_item_id)
    damaged_quantity = request.POST.get('quantity')
    if request.method == 'POST':
        form = InventoryItemForm(request.POST, instance=inventory_item)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully updated product!')
            inventory_item.total_lost_or_damaged += int(damaged_quantity)
            inventory_item.save()
            inventory_item.product.quantity -= int(damaged_quantity)
            inventory_item.product.save(update_fields=['quantity'])
            return redirect(reverse('view_inventory'))
        else:
            messages.error(request, 'Failed to update product. Please ensure the form is valid.')
    else:
        form = InventoryItemForm(instance=inventory_item)
        messages.info(request, f'You are editing {inventory_item.product.name}')

    template = 'inventory/edit_inventory_item.html'
    context = {
        'form': form,
        'inventory_item': inventory_item,
    }

    return render(request, template, context)


def auto_check_inventory_item_quantity(order):
    print(order.original_bag)

    original_bag = json.loads(order.original_bag)

    supplier_orders = {}
    for product_id, quantity in original_bag.items():
        inventory_item = InventoryItem.objects.get(product_id=product_id)
        
        supplier_name = inventory_item.supplier_name
        min_order_quantity = inventory_item.min_order_quantity
        
        if supplier_name not in supplier_orders:
            supplier_orders[supplier_name] = []
        
        supplier_orders[supplier_name].append(product_id)

    print(supplier_orders)
        # inventory_item = InventoryItem.objects.get(product_id=product_id)
        # print(inventory_item)
        # if order.original_bag[product_id] <= inventory_item.min_order_quantity:
        #     supplier_name = inventory_item.supplier_name
        #     if supplier_name not in supplier_orders:
        #         supplier_orders[supplier_name] = []
            
        #     supplier_orders[supplier_name].append(product)

    # print(supplier_orders)




    # cust_email = inventory_item.supplier_email
    # subject = render_to_string(
    #     'checkout/confirmation_emails/confirmation_email_subject.txt',
    #     {'inventory_item': inventory_item})
    # body = render_to_string(
    #     'checkout/confirmation_emails/confirmation_email_body.txt',
    #     {'inventory_item': inventory_item, 'contact_email': settings.DEFAULT_FROM_EMAIL})
    
    # send_mail(
    #     subject,
    #     body,
    #     settings.DEFAULT_FROM_EMAIL,
    #     [cust_email]
    # )

