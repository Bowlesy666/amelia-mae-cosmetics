from django.shortcuts import render


def index(request):
    """A view to return the index page"""
    return render(request, 'home/index.html')


def disclaimer(request):
    """ A view to display the disclaimer """
    return render(request, 'home/disclaimer.html')


def privacy_policy(request):
    """ A view to display the privacy policy """
    return render(request, 'home/privacy_policy.html')


def shipping_policy(request):
    """ A view to display the shipping policy """
    return render(request, 'home/shipping_policy.html')


def cookie_policy(request):
    """ A view to display the cookie policy """
    return render(request, 'home/cookie_policy.html')


def terms_and_conditions(request):
    """ A view to display the terms_and_conditions """
    return render(request, 'home/terms_and_conditions.html')


def return_and_refund_policy(request):
    """ A view to display the return_and_refund_policy """
    return render(request, 'home/return_and_refund_policy.html')
