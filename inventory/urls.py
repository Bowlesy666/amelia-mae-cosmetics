from django.urls import path
from . import views

urlpatterns = [
    path('', views.view_inventory, name='view_inventory'),
    path('edit_inventory_item/<int:inventory_item_id>/', views.edit_inventory_item, name='edit_inventory_item'),
    path('manual_stock_order/<int:inventory_item_id>/', views.manual_stock_order, name='manual_stock_order'),
    path('inbound_stock_list/', views.inbound_stock_list, name='inbound_stock_list'),
    path('inbound_stock_received/<int:inventory_item_id>/', views.inbound_stock_received, name='inbound_stock_received'),
    path('inbound_stock_cancelled/<int:inventory_item_id>/', views.inbound_stock_cancelled, name='inbound_stock_cancelled'),
]
