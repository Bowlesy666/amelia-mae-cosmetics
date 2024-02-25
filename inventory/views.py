import os
from django.db.models import Q
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.utils import timezone

from .models import InventoryItem
from .forms import InventoryItemForm
from django.conf import settings
from django.core.mail import send_mail

import json


def get_inventory_and_sorting(request, template_name):
    """
    function to show all products in inventory, including sorting
    and search queries,
    must pass the template name from view
    """
    inventory_item_list = InventoryItem.objects.all()

    query = None
    sort = None
    direction = None

    if request.GET:
        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey
            if sortkey == 'name':
                # avoid losing original field name
                sortkey = 'product__name'

            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f'-{sortkey}'
            inventory_item_list = inventory_item_list.order_by(sortkey)

        if 'is_expecting_delivery' in request.GET:
            expecting_delivery = request.GET['is_expecting_delivery']
            if expecting_delivery:
                inventory_item_list = (
                    inventory_item_list.filter(is_expecting_delivery=True))

        if 'is_not_expecting_delivery' in request.GET:
            not_expecting_delivery = request.GET['is_not_expecting_delivery']
            if not_expecting_delivery:
                inventory_item_list = (
                    inventory_item_list.filter(is_expecting_delivery=False))

        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request, "You didnt enter any search criteria!")
                return redirect(reverse('view_inventory'))

            # i before contains makes it not case sensitive
            queries = (
                Q(product__name__icontains=query) |
                Q(supplier_name__icontains=query) |
                Q(supplier_email__icontains=query)
            )
            inventory_item_list = inventory_item_list.filter(queries)

    current_sorting = f'{sort}_{direction}'

    context = {
        'search_term': query,
        'current_sorting': current_sorting,
        'inventory_item_list': inventory_item_list,
    }

    return render(request, template_name, context)


@login_required
def view_inventory(request):
    """A view that renders the inventory admin page"""
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, this action is reserved \
            for store owners only')
        return redirect(reverse('home'))
    return get_inventory_and_sorting(request, 'inventory/inventory_admin.html')


@login_required
def edit_inventory_item(request, inventory_item_id):
    """ Edit an inventory items details in the store """
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
            messages.error(
                request,
                'Failed to update product. Please ensure the form is valid.')
    else:
        form = InventoryItemForm(instance=inventory_item)
        messages.info(
            request, f'You are editing {inventory_item.product.name}')

    template = 'inventory/edit_inventory_item.html'
    context = {
        'form': form,
        'inventory_item': inventory_item,
    }

    return render(request, template, context)


@login_required
def manual_stock_order(request, inventory_item_id):
    """ View for store owners to order stock manually """
    email_path = 'inventory/supplier_restock_emails/'
    subject = os.path.join(email_path, 'manual_restock_email_subject.txt')
    body = os.path.join(email_path, 'manual_restock_email_body.txt')

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

            subject = render_to_string(subject)
            body = render_to_string(
                body,
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
    """ Automated stock ordering, checked after a product is sold """
    original_bag = json.loads(order.original_bag)

    supplier_orders = {}
    for product_id, quantity in original_bag.items():
        inventory_item = InventoryItem.objects.get(product_id=product_id)

        if not inventory_item.product.is_best_seller:
            if inventory_item.total_units_sold >= 100:
                inventory_item.product.is_best_seller = True
                inventory_item.product.save(update_fields=['is_best_seller'])

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

            inventory_items = []
            for product_id in product_ids:
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
    """ View to show items ordered from suppliers """
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
    """ View for store owners to re introduce stock after delivery """
    inventory_item = get_object_or_404(InventoryItem, pk=inventory_item_id)
    product = inventory_item.product
    ordered_quantity = inventory_item.ordered_quantity

    if request.method == 'POST':
        received_quantity_str = request.POST.get(
            f'quantity_{inventory_item.id}')
        if received_quantity_str:
            received_quantity = int(received_quantity_str)
        else:
            received_quantity = 0

        if received_quantity:
            if received_quantity > 0 and received_quantity <= ordered_quantity:
                product.quantity += received_quantity
                ordered_quantity -= received_quantity

                if product.is_out_of_stock and product.quantity >= 1:
                    product.is_out_of_stock = False
                    product.save(update_fields=['is_out_of_stock'])

                if ordered_quantity == 0:
                    inventory_item.is_expecting_delivery = False
                inventory_item.ordered_quantity = ordered_quantity
                inventory_item.save(
                    update_fields=[
                        'is_expecting_delivery', 'ordered_quantity'])

                product.save(update_fields=['quantity'])
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
    """ View to reduce inbound stock levels if 100% of order not fulfilled """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, this action is reserved \
            for store owners only')
        return redirect(reverse('home'))
    inventory_item = get_object_or_404(InventoryItem, pk=inventory_item_id)
    ordered_quantity = inventory_item.ordered_quantity

    if request.method == 'POST':
        cancelled_quantity_str = request.POST.get(
            f'quantity_{inventory_item.id}')
        if cancelled_quantity_str:
            cancelled_quantity = int(cancelled_quantity_str)

        if cancelled_quantity:
            if (cancelled_quantity > 0 and
                    cancelled_quantity <= ordered_quantity):
                ordered_quantity -= cancelled_quantity

                if ordered_quantity == 0:
                    inventory_item.is_expecting_delivery = False
                inventory_item.ordered_quantity = ordered_quantity
                inventory_item.save(
                    update_fields=[
                        'is_expecting_delivery', 'ordered_quantity'])

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
