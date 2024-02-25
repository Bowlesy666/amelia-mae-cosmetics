"""
1. `view_bag`:
   - URL pattern for viewing the contents of the shopping bag.
   - Maps to the `view_bag` view.

2. `add_to_bag`:
   - URL pattern for adding an item to the shopping bag.
   - Uses an `item_id` parameter to identify the item.
   - Maps to the `add_to_bag` view.

3. `quick_add_to_bag`:
   - URL pattern for quickly adding an item to the shopping bag.
   - Uses an `item_id` parameter to identify the item.
   - Maps to the `quick_add_to_bag` view.

4. `adjust_bag`:
   - URL pattern for adjusting the quantity of an item in the shopping bag.
   - Uses an `item_id` parameter to identify the item.
   - Maps to the `adjust_bag` view.

5. `remove_from_bag`:
   - URL pattern for removing an item from the shopping bag.
   - Uses an `item_id` parameter to identify the item.
   - Maps to the `remove_from_bag` view.
"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.view_bag, name='view_bag'),
    path('add/<item_id>/', views.add_to_bag, name='add_to_bag'),
    path(
        'quick_add/<item_id>/',
        views.quick_add_to_bag,
        name='quick_add_to_bag'
    ),
    path('adjust/<item_id>/', views.adjust_bag, name='adjust_bag'),
    path('remove/<item_id>/', views.remove_from_bag, name='remove_from_bag'),
]
