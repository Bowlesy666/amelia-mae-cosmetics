from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from checkout.models import Order
from .models import UserProfile
from .forms import UserProfileForm


@login_required
def profile(request):
    """ Display the user's profile. """
    if not request.user.is_authenticated:
        messages.error(request, 'Login to view your profile')
        redirect(reverse('home'))
    profile = get_object_or_404(UserProfile, user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')
        else:
            messages.error(
                request,
                'Update failed! Please make sure the form is valid.'
            )
    else:
        form = UserProfileForm(instance=profile)
    orders = profile.orders.filter(email=request.user.email)

    template = 'profiles/profile.html'
    context = {
        'form': form,
        'orders': orders,
        'on_profile_page': True,
    }

    return render(request, template, context)


@login_required
def order_history(request, order_number):
    """
    Display the order history for a specific order.
    """
    if not request.user.is_authenticated:
        messages.error(request, 'Login to view your profile')
        return redirect(reverse('home'))
    order = get_object_or_404(Order, order_number=order_number)

    messages.info(request, (
        f'This is a past confirmation for order number {order_number}. '
        'A confirmation email was sent on the order date.'
    ))

    template = 'checkout/checkout_success.html'
    if request.user.is_authenticated and request.user.email == order.email:
        context = {
            'order': order,
            'from_profile': True,
        }
    else:
        context = {}

    return render(request, template, context)
