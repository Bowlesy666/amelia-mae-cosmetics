from django.shortcuts import (
    render, redirect, reverse,
    HttpResponse, get_object_or_404
)
from django.http import HttpResponseRedirect
from django.contrib import messages
from products.models import Product


def view_bag(request):
    """A view that renders the bag contents page"""
    return render(request, 'bag/bag.html')


def add_to_bag(request, item_id):
    """ Add a quantity of the specified product to the shopping bag """
    product = get_object_or_404(Product, pk=item_id)
    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    bag = request.session.get('bag', {})

    if not check_in_stock(request, product, quantity, redirect_url):
        return HttpResponseRedirect(redirect_url)

    if item_id in list(bag.keys()):
        bag[item_id] += quantity
        messages.success(
            request,
            f'Updated {product.name} quantity to {bag[item_id]}'
        )
    else:
        bag[item_id] = quantity
        messages.success(request, f'Added {product.name} to your bag')

    product.quantity -= quantity
    product.save()

    request.session['bag'] = bag
    return redirect(redirect_url)


def quick_add_to_bag(request, item_id):
    """ Add 1 of specified product to the shopping bag from product list """
    product = get_object_or_404(Product, pk=item_id)
    quantity = 1
    # item_id =request.POST.get('item_id')
    redirect_url = request.POST.get('redirect_url')
    bag = request.session.get('bag', {})

    if not check_in_stock(request, product, quantity, redirect_url):
        return HttpResponseRedirect(redirect_url)

    if item_id in list(bag.keys()):
        bag[item_id] += quantity
        messages.success(
            request,
            f'Updated {product.name} quantity to {bag[item_id]}'
        )
    else:
        bag[item_id] = quantity
        messages.success(request, f'Added {product.name} to your bag')

    product.quantity -= quantity
    product.save()

    request.session['bag'] = bag
    return redirect(redirect_url)


def adjust_bag(request, item_id):
    """ Adjust quantity of the specified product to the specified amount """
    product = get_object_or_404(Product, pk=item_id)
    bag = request.session.get('bag', {})
    new_quantity = int(request.POST.get('quantity'))
    current_quantity = bag[item_id]
    # Adjusting stock by the difference of variable, minus is correct here
    quantity_difference = current_quantity - new_quantity
    redirect_to_here = reverse('view_bag')

    if quantity_difference > 0:
        check_stock = 0
    else:
        check_stock = quantity_difference

    if not check_in_stock(
        request, product,
            check_stock, redirect_to_here):
        return HttpResponseRedirect(redirect_to_here)

    if new_quantity > 0:
        product.quantity += quantity_difference
        product.save()
        bag[item_id] = new_quantity
        messages.success(
            request,
            f'Updated {product.name} quantity to {bag[item_id]}'
        )
    else:
        product.quantity -= current_quantity
        product.save()
        bag.pop(item_id)
        messages.success(request, f'Removed {product.name} from your bag')

    request.session['bag'] = bag
    return redirect(redirect_to_here)


def check_in_stock(request, product, requested_quantity, redirect_to_here):
    """ Check if product has enough stock before adding to bag """
    if product.quantity < requested_quantity:
        messages.error(
            request,
            f'There does not seem to be enough {product.name}, \
                to add it to your bag. Please try a differnet amount'
        )
        return False
    else:
        return True


def remove_from_bag(request, item_id):
    """ Remove unwanted items from checkout """
    try:
        product = get_object_or_404(Product, pk=item_id)
        bag = request.session.get('bag', {})
        quantity = bag[item_id]
        bag.pop(item_id)
        messages.success(request, f'Removed {product.name} from your bag')

        product.quantity += quantity
        product.save()

        request.session['bag'] = bag
        return HttpResponse(status=200)

    except Exception as e:
        messages.error(request, f'Error removing item: {e}')
        return HttpResponse(status=500)
