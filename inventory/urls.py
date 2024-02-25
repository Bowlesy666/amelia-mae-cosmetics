"""
1. `view_inventory`:
   - URL pattern for viewing the inventory.
   - Maps to the `view_inventory` view.

2. `edit_inventory_item`:
   - URL pattern for editing an inventory item.
   - Uses an inventory item ID parameter to identify the item.
   - Maps to the `edit_inventory_item` view.

3. `manual_stock_order`:
   - URL pattern for manually placing a stock order for an inventory item.
   - Uses an inventory item ID parameter to identify the item.
   - Maps to the `manual_stock_order` view.

4. `inbound_stock_list`:
   - URL pattern for viewing the list of inbound stock.
   - Maps to the `inbound_stock_list` view.

5. `inbound_stock_received`:
   - URL pattern for marking inbound stock as received for an inventory item.
   - Uses an inventory item ID parameter to identify the item.
   - Maps to the `inbound_stock_received` view.

6. `inbound_stock_cancelled`:
   - URL pattern for cancelling inbound stock for an inventory item.
   - Uses an inventory item ID parameter to identify the item.
   - Maps to the `inbound_stock_cancelled` view.
"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.view_inventory, name='view_inventory'),
    path(
        'edit_inventory_item/<int:inventory_item_id>/',
        views.edit_inventory_item,
        name='edit_inventory_item'
    ),
    path(
        'manual_stock_order/<int:inventory_item_id>/',
        views.manual_stock_order,
        name='manual_stock_order'
    ),
    path(
        'inbound_stock_list/',
        views.inbound_stock_list,
        name='inbound_stock_list'
    ),
    path(
        'inbound_stock_received/<int:inventory_item_id>/',
        views.inbound_stock_received,
        name='inbound_stock_received'
    ),
    path(
        'inbound_stock_cancelled/<int:inventory_item_id>/',
        views.inbound_stock_cancelled,
        name='inbound_stock_cancelled'
    ),
]
