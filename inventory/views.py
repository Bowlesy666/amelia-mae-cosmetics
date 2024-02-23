from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.utils import timezone

from products.views import get_products_and_sorting
from .models import InventoryItem
from products.models import Product
from .forms import InventoryItemForm
from django.conf import settings
from django.core.mail import send_mail

import json


@login_required
def view_inventory(request):
    """A view that renders the inventory admin page"""
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, this action is reserved \
            for store owners only')
        return redirect(reverse('home'))
    return get_products_and_sorting(request, 'inventory/inventory_admin.html')


@login_required
def edit_inventory_item(request, inventory_item_id):
    """ Edit a inventory items details in the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, this action is reserved \
            for store owners only')
        return redirect(reverse('home'))
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


@login_required
def manual_stock_order(request, inventory_item_id):
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, this action is reserved \
            for store owners only')
        return redirect(reverse('home'))
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
        discontinued = inventory_item.product.is_discontinued
        if (total_stock <= min_threshold and 
            not expecting_delivery and 
            not discontinued):

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


@login_required
def inbound_stock_list(request):
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, this action is reserved \
            for store owners only')
        return redirect(reverse('home'))
    inventory_items = InventoryItem.objects.filter(is_expecting_delivery=True)

    template = 'inventory/inbound_stock_list.html'

    context = {
        'inventory_items': inventory_items,
    }

    messages.info(request, 'Please accurately update stock')
    return render(request, template, context)


def inbound_stock_received(request, inventory_item_id):
    inventory_item = get_object_or_404(InventoryItem, pk=inventory_item_id)
    product = inventory_item.product
    ordered_quantity = inventory_item.ordered_quantity

    if request.method == 'POST':
        print('POST')
        received_quantity_str = request.POST.get(
            f'quantity_{inventory_item.id}')
        if received_quantity_str:
            received_quantity = int(received_quantity_str)
        else:
            received_quantity = 0
        print('Received_quantity str', received_quantity_str)
        print('Received_quantity', received_quantity)

        if received_quantity:
            print('received!')
            if received_quantity > 0 and received_quantity <= ordered_quantity:
                product.quantity += received_quantity
                print('ordered quantity before:', ordered_quantity)
                ordered_quantity -= received_quantity
                print('ordered quantity after:', ordered_quantity)

                if ordered_quantity == 0:
                    inventory_item.is_expecting_delivery = False
                inventory_item.ordered_quantity = ordered_quantity
                inventory_item.save(update_fields=['is_expecting_delivery', 'ordered_quantity'])
                print('ordered quantity saved:', ordered_quantity)

                product.save(update_fields=['quantity'])
                print('Product quantity saved:', product.quantity)
                messages.success(
                    request, f'{received_quantity} units received for \
                        {inventory_item.product.name}.')
            else:
                messages.error(request, 'Please enter a valid quantity, \
                    from 1 up to the requested amount. \
                    Surplus stock must be taken to procurement \
                        for investigation.')
        return redirect(reverse('inbound_stock_list'))
    else:
        messages.info(request, 'Please accurately update stock')
        return redirect(reverse('inbound_stock_list'))


@login_required
def inbound_stock_cancelled(request, inventory_item_id):
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, this action is reserved \
            for store owners only')
        return redirect(reverse('home'))
    inventory_item = get_object_or_404(InventoryItem, pk=inventory_item_id)
    product = inventory_item.product
    ordered_quantity = inventory_item.ordered_quantity

    if request.method == 'POST':
        print('POST')
        cancelled_quantity_str = request.POST.get(
            f'quantity_{inventory_item.id}')
        if cancelled_quantity_str:
            cancelled_quantity = int(cancelled_quantity_str)
        else:
            received_quantity = 0
        print('cancelled_quantity str', cancelled_quantity_str)
        print('cancelled_quantity', cancelled_quantity)

        if cancelled_quantity:
            print('cancelled!')
            if cancelled_quantity > 0 and cancelled_quantity <= ordered_quantity:
                print('quantity before:', product.quantity)
                ordered_quantity -= cancelled_quantity
                print('ordered quantity after:', ordered_quantity)

                if ordered_quantity == 0:
                    inventory_item.is_expecting_delivery = False
                inventory_item.ordered_quantity = ordered_quantity
                inventory_item.save(update_fields=['is_expecting_delivery', 'ordered_quantity'])
                print('product quantity saved:', product.quantity)

                messages.success(
                    request, f'{cancelled_quantity} units cancelled for \
                        {inventory_item.product.name}.')
            else:
                messages.error(request, 'Please enter a valid quantity, \
                    from 1 up to the requested amount. \
                    Surplus stock must be taken to procurement \
                        for investigation.')
        return redirect(reverse('inbound_stock_list'))
    else:
        messages.info(request, 'Please accurately update stock')
        return redirect(reverse('inbound_stock_list'))

