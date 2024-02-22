from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.template.loader import render_to_string
from django.utils import timezone

from products.views import get_products_and_sorting
from .models import InventoryItem
from products.models import Product
from .forms import InventoryItemForm
from django.conf import settings
from django.core.mail import send_mail

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


def manual_stock_order(request, inventory_item_id):
    inventory_item = get_object_or_404(InventoryItem, pk=inventory_item_id)
    template = 'inventory/manual_stock_order.html'

    if request.method == 'POST':
        order_quantity_str = request.POST.get('quantity')
        if order_quantity_str:
            order_quantity = int(order_quantity_str)
        else:
            order_quantity = 0
        print('POST')
        print('order quantity: ', order_quantity)
        if order_quantity < 1000 and order_quantity > 0:
            inventory_item.is_expecting_delivery = True
            inventory_item.last_reorder_date = timezone.now()
            inventory_item.ordered_quantity += order_quantity
            inventory_item.save(
                update_fields=[
                    'is_expecting_delivery', 'last_reorder_date',
                    'ordered_quantity'])
            messages.success(request, f'Purchase order Successful! \
                { inventory_item.product.name } x { order_quantity }') 
            cust_email = inventory_item.supplier_email

            subject = render_to_string(
                'inventory/supplier_restock_emails/manual_restock_email_subject.txt')
            body = render_to_string(
                'inventory/supplier_restock_emails/manual_restock_email_body.txt',
                {'inventory_item': inventory_item,
                'order_quantity': order_quantity,
                'contact_email': settings.DEFAULT_FROM_EMAIL})
            
            send_mail(
                subject,
                body,
                settings.DEFAULT_FROM_EMAIL,
                [cust_email]
            )

            return redirect(reverse('view_inventory'))
        else:
            messages.error(request, 'Failed to send purchase order. \
                Please select a quantity between 1 and 1000. \
                For higher quantities please consult procurement team.')
    else:
        messages.info(request, f'You are creating a purchase order for: \
            {inventory_item.product.name}')
        
    context = {
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
        total_stock = inventory_item.product.quantity
        min_threshold = inventory_item.min_threshold

        total_units_sold = inventory_item.total_units_sold
        total_units_sold += quantity
        inventory_item.total_units_sold = total_units_sold

        sale_price = inventory_item.product.price
        trade_cost = inventory_item.cost_per_product

        total_revenue_generated = (
            (total_units_sold * sale_price) - (total_units_sold * trade_cost))
        inventory_item.total_revenue_generated = total_revenue_generated
        inventory_item.save(
            update_fields=['total_units_sold', 'total_revenue_generated'])
        expecting_delivery = inventory_item.is_expecting_delivery
        if total_stock <= min_threshold and not expecting_delivery:
            if supplier_name not in supplier_orders:
                supplier_orders[supplier_name] = []
            
            supplier_orders[supplier_name].append(product_id)

    if supplier_orders:
        for supplier_name, product_ids in supplier_orders.items():

            products = []
            inventory_items = []
            for product_id in product_ids:
                product = get_object_or_404(Product, id=product_id)
                inventory_item = get_object_or_404(
                    InventoryItem, product_id=product_id)
                inventory_item.is_expecting_delivery = True
                inventory_item.last_reorder_date = timezone.now()
                order_quantity = inventory_item.min_order_quantity
                inventory_item.ordered_quantity += order_quantity
                inventory_item.save(
                    update_fields=[
                        'is_expecting_delivery', 'last_reorder_date',
                        'ordered_quantity'])

                inventory_items.append(inventory_item)

            cust_email = inventory_items[0].supplier_email
            subject = render_to_string(
                'inventory/supplier_restock_emails/restock_email_subject.txt')
            body = render_to_string(
                'inventory/supplier_restock_emails/restock_email_body.txt',
                {'supplier_name': supplier_name,
                'inventory_items': inventory_items,
                'contact_email': settings.DEFAULT_FROM_EMAIL})
            
            send_mail(
                subject,
                body,
                settings.DEFAULT_FROM_EMAIL,
                [cust_email]
            )


def inbound_stock_recieved(request, inventory_item_id, quantity):
    inventory_item = get_object_or_404(InventoryItem, pk=inventory_item_id)
    inventory_items = InventoryItem.objects.filter('is_expecting_delivery')
    product = inventory_item.product

    template = 'inventory/inbound_stock_list.html'

    context = {
        'inventory_items': inventory_items,
    }

    if request.method == 'POST':
        received_quantity = request.POST.get(f'quantity_{inventory_item_id}')

        if received_quantity:
            received_quantity = int(received_quantity)
            if received_quantity > 0 and received_quantity <= quantity:
                product.quantity += quantity
                if received_quantity == quantity:
                    inventory_item.is_expecting_delivery = False
                    inventory_item.save(
                        update_fields=['is_expecting_delivery'])
                product.save(update_fields=['quantity'])
                messages.success(
                    request, f'{received_quantity} units received for \
                        {inventory_item.product.name}.')
            else:
                messages.error(request, 'Please enter a valid quantity, \
                    from 1 up to the requested amount. \
                    Surplus stock must be taken to procurement \
                        for investigation.')
        return render(request, template, context)
    else:
        messages.info(request, 'Please accurately update stock received')
        return render(request, template, context)
