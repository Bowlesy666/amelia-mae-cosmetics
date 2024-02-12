from django.shortcuts import render, redirect, reverse
from django.contrib import messages
import os

from .forms import OrderForm


def checkout(request):
    bag = request.session.get('bag', {})
    if not bag:
        messages.error(request, "Your shopping bag is empty")
        return redirect(reverse('products'))

    order_form = OrderForm()
    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': os.environ.get('STRIPE_PUBLIC_KEY'),
        'client_secret': os.environ.get('STRIPE_SECRET_KEY'),
    }

    return render(request, template, context)
