"""
1. `checkout`:
   - URL pattern for accessing the checkout page.
   - Maps to the `checkout` view.

2. `checkout_success`:
   - URL pattern for displaying the checkout success page.
   - Uses an `order_number` parameter to identify the order.
   - Maps to the `checkout_success` view.

3. `cache_checkout_data`:
   - URL pattern for caching checkout data.
   - Maps to the `cache_checkout_data` view.

4. `webhook`:
   - URL pattern for handling webhook requests.
   - Maps to the `webhook` view, which handles webhook events.
"""
from django.urls import path
from . import views
from .webhooks import webhook

urlpatterns = [
    path('', views.checkout, name='checkout'),
    path(
        'checkout_success/<order_number>/',
        views.checkout_success,
        name='checkout_success'
    ),
    path(
        'cache_checkout_data/',
        views.cache_checkout_data,
        name='cache_checkout_data'
    ),
    path('wh/', webhook, name='webhook'),
]
