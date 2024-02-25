"""
1. `profile`:
   - URL pattern for displaying the user's profile.
   - Maps to the `profile` view.

2. `order_history`:
   - URL pattern for viewing the order history for a specific order.
   - Uses an order number parameter to identify the order.
   - Maps to the `order_history` view.
"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.profile, name='profile'),
    path(
        'order_history/<order_number>/',
        views.order_history,
        name='order_history'
    ),
]
